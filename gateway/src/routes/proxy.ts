import { FastifyInstance, FastifyRequest, FastifyReply } from 'fastify';
import { sanitizePayload } from '../middlewares/pii_sanitizer';

const JAVA_CORE_URL = process.env.JAVA_CORE_URL || 'http://localhost:8081';
const AI_CORE_URL = process.env.AI_CORE_URL || 'http://localhost:8000';

export async function proxyRoutes(fastify: FastifyInstance) {
  /**
   * Rota de Transações Financeiras -> Roteia para o Core Java 21 (Spring Boot)
   */
  fastify.post('/api/v1/transacoes', async (request: FastifyRequest, reply: FastifyReply) => {
    try {
      const sanitizedBody = sanitizePayload(request.body);
      const javaResponse = await fetch(`${JAVA_CORE_URL}/api/v1/transacoes`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': request.headers.authorization || ''
        },
        body: JSON.stringify(sanitizedBody)
      });

      const data = await javaResponse.json();
      return reply.status(javaResponse.status).send(data);
    } catch (err: any) {
      fastify.log.error(err, 'Erro ao conectar com Transactional Core (Java)');
      return reply.status(503).send({
        error: 'Service Unavailable',
        message: 'Transactional Core indisponível no momento.'
      });
    }
  });

  /**
   * Rota de Diagnóstico de POS -> Roteia para o AI Core (Python FastAPI)
   */
  fastify.post('/api/v1/diagnosis/pos', async (request: FastifyRequest, reply: FastifyReply) => {
    try {
      const sanitizedBody = sanitizePayload(request.body);
      const aiResponse = await fetch(`${AI_CORE_URL}/api/v1/diagnosis/pos`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(sanitizedBody)
      });

      const data = await aiResponse.json();
      return reply.status(aiResponse.status).send(data);
    } catch (err: any) {
      fastify.log.error(err, 'Erro ao conectar com AI Core');
      return reply.status(503).send({
        error: 'Service Unavailable',
        message: 'AI Core indisponível no momento.'
      });
    }
  });
}
