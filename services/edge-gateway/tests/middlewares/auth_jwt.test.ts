import { FastifyRequest, FastifyReply } from 'fastify';
import { authenticateJWT } from '../../src/middlewares/auth_jwt';

describe('Auth JWT Middleware (1:1 tests)', () => {
  let mockReply: Partial<FastifyReply>;
  let statusMock: jest.Mock;
  let sendMock: jest.Mock;

  beforeEach(() => {
    sendMock = jest.fn();
    statusMock = jest.fn().mockReturnValue({ send: sendMock });
    mockReply = {
      status: statusMock,
      send: sendMock
    };
  });

  it('deve permitir acesso direto para rotas públicas como /health e /', async () => {
    const reqHealth = { url: '/health', headers: {} } as FastifyRequest;
    const reqRoot = { url: '/', headers: {} } as FastifyRequest;

    await authenticateJWT(reqHealth, mockReply as FastifyReply);
    await authenticateJWT(reqRoot, mockReply as FastifyReply);

    expect(statusMock).not.toHaveBeenCalled();
    expect(sendMock).not.toHaveBeenCalled();
  });

  it('deve retornar 401 Unauthorized se header Authorization estiver ausente', async () => {
    const req = { url: '/api/v1/protected', headers: {} } as FastifyRequest;

    await authenticateJWT(req, mockReply as FastifyReply);

    expect(statusMock).toHaveBeenCalledWith(401);
    expect(sendMock).toHaveBeenCalledWith(
      expect.objectContaining({
        error: 'Unauthorized',
        message: 'Header Authorization (Bearer token) é obrigatório.'
      })
    );
  });

  it('deve retornar 401 Unauthorized se o token não estiver no formato Bearer', async () => {
    const req = {
      url: '/api/v1/protected',
      headers: { authorization: 'Basic 12345' }
    } as FastifyRequest;

    await authenticateJWT(req, mockReply as FastifyReply);

    expect(statusMock).toHaveBeenCalledWith(401);
    expect(sendMock).toHaveBeenCalledWith(
      expect.objectContaining({
        error: 'Unauthorized',
        message: 'Formato inválido do token Bearer.'
      })
    );
  });

  it('deve anexar payload do usuário na requisição quando o token Bearer for válido', async () => {
    const req = {
      url: '/api/v1/protected',
      headers: { authorization: 'Bearer valid-jwt-token' }
    } as any;

    await authenticateJWT(req, mockReply as FastifyReply);

    expect(statusMock).not.toHaveBeenCalled();
    expect(req.user).toEqual({
      userId: 'user_stone_mock',
      lojistaId: 'lojista_123',
      role: 'MERCHANT_ADMIN'
    });
  });
});
