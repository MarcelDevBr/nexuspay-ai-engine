import { FastifyInstance, FastifyRequest, FastifyReply } from 'fastify';
import { sanitizePayload } from '../middlewares/pii_sanitizer';

const AI_CORE_URL = process.env.AI_CORE_URL || 'http://localhost:8000';

export async function sseStreamRoutes(fastify: FastifyInstance) {
  /**
   * Endpoint de Streaming SSE para o Copilot Financeiro RAG
   * Recebe a pergunta do lojista, sanitiza dados sensíveis e abre um stream token a token
   */
  fastify.post('/api/v1/chat/stream', async (request: FastifyRequest, reply: FastifyReply) => {
    const rawBody = request.body as any;

    if (!rawBody || !rawBody.prompt) {
      return reply.status(400).send({
        error: 'Bad Request',
        message: 'Campo "prompt" é obrigatório.'
      });
    }

    // 1. Sanitização PII (PCI-DSS)
    const sanitizedBody = sanitizePayload(rawBody);

    // 2. Configura headers para Server-Sent Events (SSE)
    reply.raw.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'Access-Control-Allow-Origin': '*'
    });

    try {
      // 3. Encaminha requisição para o AI Core (FastAPI)
      const aiResponse = await fetch(`${AI_CORE_URL}/api/v1/chat/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(sanitizedBody)
      });

      if (!aiResponse.ok || !aiResponse.body) {
        reply.raw.write(`data: ${JSON.stringify({ error: 'Falha ao conectar com o motor de IA.' })}\n\n`);
        reply.raw.end();
        return;
      }

      // 4. Stream direto token-a-token
      const reader = aiResponse.body.getReader();
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
      fastify.log.error(err, 'Erro durante streaming SSE com AI Core');
      reply.raw.write(`data: ${JSON.stringify({ error: 'Erro de comunicação interna.' })}\n\n`);
      reply.raw.end();
    }
  });
}
