import { FastifyInstance } from 'fastify';

export async function healthRoutes(fastify: FastifyInstance) {
  fastify.get('/health', async () => {
    return {
      status: 'UP',
      service: 'nexuspay-edge-gateway',
      version: '1.0.0',
      timestamp: new Date().toISOString(),
      uptime: process.uptime()
    };
  });

  fastify.get('/', async () => {
    return {
      name: 'NexusPay AI Engine - Edge API Gateway',
      docs: '/docs',
      status: 'operational'
    };
  });
}
