import Fastify from 'fastify';
import { proxyRoutes } from '../../src/routes/proxy';

describe('Proxy Routes (1:1 tests)', () => {
  let app: any;
  const originalFetch = global.fetch;

  beforeAll(async () => {
    app = Fastify();
    await app.register(proxyRoutes);
    await app.ready();
  });

  afterAll(async () => {
    await app.close();
  });

  afterEach(() => {
    global.fetch = originalFetch;
  });

  it('deve repassar transação para transaction-ledger-service com sucesso', async () => {
    global.fetch = jest.fn().mockResolvedValue({
      status: 201,
      ok: true,
      json: async () => ({ id: 'tx-123', status: 'AUTORIZADO' })
    } as any);

    const response = await app.inject({
      method: 'POST',
      url: '/api/v1/transacoes',
      payload: {
        lojistaId: 'lojista_123',
        valor: 100.00,
        numeroCartao: '4111222233334444'
      }
    });

    expect(response.statusCode).toBe(201);
    expect(JSON.parse(response.payload).id).toBe('tx-123');
  });

  it('deve retornar 503 quando transaction-ledger-service estiver indisponível', async () => {
    global.fetch = jest.fn().mockRejectedValue(new Error('Connection failure to Java service'));

    const response = await app.inject({
      method: 'POST',
      url: '/api/v1/transacoes',
      payload: { lojistaId: 'lojista_123', valor: 50.00 }
    });

    expect(response.statusCode).toBe(503);
    const body = JSON.parse(response.payload);
    expect(body.error).toBe('Service Unavailable');
    expect(body.message).toContain('Transaction Ledger Service indisponível');
  });

  it('deve repassar diagnóstico de POS para pos-diagnostics-service com sucesso', async () => {
    global.fetch = jest.fn().mockResolvedValue({
      status: 200,
      ok: true,
      json: async () => ({ status: 'RESOLVED', diagnostic: 'OK' })
    } as any);

    const response = await app.inject({
      method: 'POST',
      url: '/api/v1/diagnosis/pos',
      payload: { terminalId: 'term-1', errorCode: 'ERR_58' }
    });

    expect(response.statusCode).toBe(200);
    expect(JSON.parse(response.payload).status).toBe('RESOLVED');
  });

  it('deve retornar 503 quando pos-diagnostics-service falhar', async () => {
    global.fetch = jest.fn().mockRejectedValue(new Error('POS connection error'));

    const response = await app.inject({
      method: 'POST',
      url: '/api/v1/diagnosis/pos',
      payload: { terminalId: 'term-1' }
    });

    expect(response.statusCode).toBe(503);
    const body = JSON.parse(response.payload);
    expect(body.error).toBe('Service Unavailable');
    expect(body.message).toContain('POS Diagnostics Service indisponível');
  });
});
