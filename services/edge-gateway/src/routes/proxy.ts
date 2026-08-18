import { FastifyInstance, FastifyRequest, FastifyReply } from 'fastify';
import { sanitizePayload } from '../middlewares/pii_sanitizer';

const TRANSACTION_SERVICE_URL = process.env.TRANSACTION_SERVICE_URL || 'http://localhost:8081';
const DIAGNOSTICS_SERVICE_URL = process.env.DIAGNOSTICS_SERVICE_URL || 'http://localhost:8002';

export async function proxyRoutes(fastify: FastifyInstance) {
  /**
   * Rota de Transações Financeiras -> Roteia para o transaction-ledger-service (Java 26)
   */
  fastify.post('/api/v1/transacoes', async (request: FastifyRequest, reply: FastifyReply) => {
    try {
      const sanitizedBody = sanitizePayload(request.body);
      const javaResponse = await fetch(`${TRANSACTION_SERVICE_URL}/api/v1/transacoes`, {
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
      fastify.log.error(err, 'Erro ao conectar com Transaction Ledger Service');
      return reply.status(503).send({
        error: 'Service Unavailable',
        message: 'Transaction Ledger Service indisponível no momento.'
      });
    }
  });

  /**
   * Rota de Diagnóstico de POS -> Roteia para o pos-diagnostics-service (Python 3.14)
   */
  fastify.post('/api/v1/diagnosis/pos', async (request: FastifyRequest, reply: FastifyReply) => {
    try {
      const sanitizedBody = sanitizePayload(request.body);
      const diagResponse = await fetch(`${DIAGNOSTICS_SERVICE_URL}/api/v1/diagnosis/pos`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(sanitizedBody)
      });

      const data = await diagResponse.json();
      return reply.status(diagResponse.status).send(data);
    } catch (err: any) {
      fastify.log.error(err, 'Erro ao conectar com POS Diagnostics Service');
      return reply.status(503).send({
        error: 'Service Unavailable',
        message: 'POS Diagnostics Service indisponível no momento.'
      });
    }
  });
}
