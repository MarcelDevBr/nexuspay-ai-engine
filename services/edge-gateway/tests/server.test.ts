import { buildApp } from '../src/server';

describe('Server & Fastify App Builder (1:1 tests)', () => {
  let app: any;

  beforeAll(async () => {
    app = await buildApp();
  });

  afterAll(async () => {
    await app.close();
  });

  it('deve inicializar a instância do Fastify com middlewares e rotas registradas', async () => {
    expect(app).toBeDefined();
    expect(typeof app.inject).toBe('function');
  });

  it('deve bloquear requisições para rotas protegidas sem autenticação', async () => {
    const res = await app.inject({
      method: 'POST',
      url: '/api/v1/transacoes',
      payload: { lojistaId: 'loj_123', valor: 10.0 }
    });

    expect(res.statusCode).toBe(401);
  });

  it('deve permitir requisições para rotas públicas sem autenticação', async () => {
    const res = await app.inject({
      method: 'GET',
      url: '/health'
    });

    expect(res.statusCode).toBe(200);
  });
});
