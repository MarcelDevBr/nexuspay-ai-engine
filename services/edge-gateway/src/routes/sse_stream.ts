import { FastifyInstance, FastifyRequest, FastifyReply } from 'fastify';
import { sanitizePayload } from '../middlewares/pii_sanitizer';

const COPILOT_SERVICE_URL = process.env.COPILOT_SERVICE_URL || 'http://localhost:8000';

export async function sseStreamRoutes(fastify: FastifyInstance) {
  fastify.post('/api/v1/chat/stream', async (request: FastifyRequest, reply: FastifyReply) => {
    const rawBody = request.body as any;

    if (!rawBody || !rawBody.prompt) {
      return reply.status(400).send({
        error: 'Bad Request',
        message: 'Campo "prompt" é obrigatório.'
      });
    }

    const sanitizedBody = sanitizePayload(rawBody);

    reply.raw.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'Access-Control-Allow-Origin': '*'
    });

    try {
      const copilotResponse = await fetch(`${COPILOT_SERVICE_URL}/api/v1/chat/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(sanitizedBody)
      });

      if (!copilotResponse.ok || !copilotResponse.body) {
        reply.raw.write(`data: ${JSON.stringify({ error: 'Falha ao conectar com o Copilot RAG Service.' })}\n\n`);
        reply.raw.end();
        return;
      }

      const reader = copilotResponse.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          reply.raw.write(`data: [DONE]\n\n`);
          break;
        }
        const chunk = decoder.decode(value, { stream: true });
        reply.raw.write(chunk);
      }

      reply.raw.end();
    } catch (err: any) {
      fastify.log.error(err, 'Erro durante streaming SSE com Copilot Service');
      reply.raw.write(`data: ${JSON.stringify({ error: 'Erro de comunicação interna.' })}\n\n`);
      reply.raw.end();
    }
  });
}
