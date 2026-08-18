import Fastify from 'fastify';
import { healthRoutes } from '../../src/routes/health';

describe('Health Routes (1:1 tests)', () => {
  let app: any;

  beforeAll(async () => {
    app = Fastify();
    await app.register(healthRoutes);
    await app.ready();
  });

  afterAll(async () => {
    await app.close();
  });

  it('deve responder 200 OK no endpoint /health', async () => {
    const res = await app.inject({
      method: 'GET',
      url: '/health'
    });

    expect(res.statusCode).toBe(200);
    const body = JSON.parse(res.payload);
    expect(body.status).toBe('UP');
    expect(body.service).toBe('nexuspay-edge-gateway');
    expect(body.timestamp).toBeDefined();
  });

  it('deve responder 200 OK no endpoint raiz /', async () => {
    const res = await app.inject({
      method: 'GET',
      url: '/'
    });

    expect(res.statusCode).toBe(200);
    const body = JSON.parse(res.payload);
    expect(body.status).toBe('operational');
    expect(body.name).toContain('NexusPay');
  });
});
