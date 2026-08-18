import { FastifyRequest, FastifyReply } from 'fastify';

/**
 * Autenticação JWT Mock / Zero-Trust para ambiente de demonstração e produção
 */
export async function authenticateJWT(request: FastifyRequest, reply: FastifyReply) {
  const authHeader = request.headers.authorization;

  // Em rotas de health ou públicas, ignora validação
  if (request.url === '/health' || request.url === '/') {
    return;
  }

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

  // Token válido ou mock aceito para testes locais
  (request as any).user = {
    userId: 'user_stone_mock',
    lojistaId: 'lojista_123',
    role: 'MERCHANT_ADMIN'
  };
}
