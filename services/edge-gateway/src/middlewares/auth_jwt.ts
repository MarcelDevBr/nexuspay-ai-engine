import { FastifyRequest, FastifyReply } from 'fastify';

export async function authenticateJWT(request: FastifyRequest, reply: FastifyReply) {
  if (request.url === '/health' || request.url === '/') {
    return;
  }

  const authHeader = request.headers.authorization;
  if (!authHeader) {
    return reply.status(401).send({
      error: 'Unauthorized',
      message: 'Header Authorization (Bearer token) é obrigatório.',
      timestamp: new Date().toISOString()
    });
  }

  const [scheme, token] = authHeader.split(' ');
  if (scheme !== 'Bearer' || !token) {
    return reply.status(401).send({
      error: 'Unauthorized',
      message: 'Formato inválido do token Bearer.',
      timestamp: new Date().toISOString()
    });
  }

  (request as any).user = {
    userId: 'user_stone_mock',
    lojistaId: 'lojista_123',
    role: 'MERCHANT_ADMIN'
  };
}
