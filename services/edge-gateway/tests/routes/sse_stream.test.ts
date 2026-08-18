import Fastify from 'fastify';
import { sseStreamRoutes } from '../../src/routes/sse_stream';

describe('SSE Stream Routes (1:1 tests)', () => {
  let app: any;
  const originalFetch = global.fetch;

  beforeAll(async () => {
    app = Fastify();
    await app.register(sseStreamRoutes);
    await app.ready();
  });

  afterAll(async () => {
    await app.close();
  });

  afterEach(() => {
    global.fetch = originalFetch;
  });

  it('deve retornar 400 Bad Request se prompt não for informado', async () => {
    const res = await app.inject({
      method: 'POST',
      url: '/api/v1/chat/stream',
      payload: { lojistaId: 'loj-1' }
    });

    expect(res.statusCode).toBe(400);
    const body = JSON.parse(res.payload);
    expect(body.error).toBe('Bad Request');
  });

  it('deve processar e transmitir stream SSE com sucesso', async () => {
    const encoder = new TextEncoder();
    const chunks = [
      encoder.encode('data: {"token": "Olá"}\n\n'),
      encoder.encode('data: [DONE]\n\n')
    ];
    let index = 0;

    const mockBody = {
      getReader: () => ({
        read: async () => {
          if (index < chunks.length) {
            return { done: false, value: chunks[index++] };
          }
          return { done: true, value: undefined };
        }
      })
    };

    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      body: mockBody
    } as any);

    const res = await app.inject({
      method: 'POST',
      url: '/api/v1/chat/stream',
      payload: { lojistaId: 'loj-1', prompt: 'Qual é a taxa Pix?' }
    });

    expect(res.statusCode).toBe(200);
    expect(res.headers['content-type']).toContain('text/event-stream');
    expect(res.payload).toContain('data: {"token": "Olá"}');
  });

  it('deve tratar resposta não-OK do Copilot RAG Service', async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: false,
      body: null
    } as any);

    const res = await app.inject({
      method: 'POST',
      url: '/api/v1/chat/stream',
      payload: { lojistaId: 'loj-1', prompt: 'Dúvida' }
    });

    expect(res.statusCode).toBe(200);
    expect(res.payload).toContain('Falha ao conectar com o Copilot RAG Service');
  });

  it('deve capturar e tratar erro de rede durante o streaming SSE', async () => {
    global.fetch = jest.fn().mockRejectedValue(new Error('Network break'));

    const res = await app.inject({
      method: 'POST',
      url: '/api/v1/chat/stream',
      payload: { lojistaId: 'loj-1', prompt: 'Dúvida com erro' }
    });

    expect(res.statusCode).toBe(200);
    expect(res.payload).toContain('Erro de comunicação interna');
  });
});
