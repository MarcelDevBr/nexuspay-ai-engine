import Fastify from 'fastify';
import cors from '@fastify/cors';
import helmet from '@fastify/helmet';
import rateLimit from '@fastify/rate-limit';
import { healthRoutes } from './routes/health';
import { sseStreamRoutes } from './routes/sse_stream';
import { proxyRoutes } from './routes/proxy';
import { authenticateJWT } from './middlewares/auth_jwt';

const PORT = parseInt(process.env.PORT || '8080', 10);
const HOST = process.env.HOST || '0.0.0.0';

export async function buildApp() {
  const fastify = Fastify({
    logger: {
      level: process.env.LOG_LEVEL || 'info'
    }
  });

  await fastify.register(helmet, { contentSecurityPolicy: false });
  await fastify.register(cors, { origin: true });

  await fastify.register(rateLimit, {
    max: 1000,
    timeWindow: '1 minute'
  });

  fastify.addHook('onRequest', authenticateJWT);

  await fastify.register(healthRoutes);
  await fastify.register(sseStreamRoutes);
  await fastify.register(proxyRoutes);

  return fastify;
}

if (require.main === module) {
  buildApp().then(app => {
    app.listen({ port: PORT, host: HOST }, (err, address) => {
      if (err) {
        app.log.error(err);
        process.exit(1);
      }
      app.log.info(`🚀 NexusPay Edge Gateway rodando em ${address}`);
    });
  });
}
