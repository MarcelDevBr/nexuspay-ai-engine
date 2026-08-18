import { sanitizePayload, maskCreditCard, maskCPF, maskCVV } from '../src/middlewares/pii_sanitizer';
import { buildApp } from '../src/server';

describe('PII Sanitizer & PCI-DSS Guardrails', () => {
  it('deve mascarar número de cartão de crédito deixando apenas os últimos 4 dígitos', () => {
    const raw = 'O cliente pagou com o cartão 4111 2222 3333 4444 no POS';
    const sanitized = maskCreditCard(raw);
    expect(sanitized).toBe('O cliente pagou com o cartão [CARD_FINAL_4444] no POS');
  });

  it('deve mascarar CPF formatado e numérico', () => {
    const raw = 'O CPF do lojista é 123.456.789-00';
    const sanitized = maskCPF(raw);
    expect(sanitized).toBe('O CPF do lojista é [CPF_PROTEGIDO]');
  });

  it('deve mascarar CVV explicitamente', () => {
    const raw = 'cvv: 999';
    expect(maskCVV(raw)).toBe('cvv: [REDACTED]');
  });

  it('deve lidar com valores primitivos e não-strings no sanitizePayload', () => {
    expect(sanitizePayload(null)).toBeNull();
    expect(sanitizePayload(12345)).toBe(12345);
    expect(sanitizePayload([123, '4111222233334444'])).toEqual([123, '[CARD_FINAL_4444]']);
    expect(maskCreditCard(123 as any)).toBe(123 as any);
    expect(maskCPF(123 as any)).toBe(123 as any);
    expect(maskCVV(123 as any)).toBe(123 as any);
    expect(maskCreditCard('123456789012')).toBe('123456789012');
  });

  it('deve sanitizar objetos JSON aninhados com CVV e dados sensíveis', () => {
    const payload = {
      lojistaId: 'lojista_123',
      prompt: 'Comprovante da venda com cartão 5502099988881234 e CPF 111.222.333-44',
      card_details: {
        cvv: '123',
        holder: 'MARCEL ALMEIDA'
      }
    };

    const sanitized = sanitizePayload(payload);
    expect(sanitized.prompt).toContain('[CARD_FINAL_1234]');
    expect(sanitized.prompt).toContain('[CPF_PROTEGIDO]');
    expect(sanitized.card_details.cvv).toBe('[REDACTED]');
  });
});

describe('Edge Gateway HTTP Routes & Server', () => {
  let app: any;

  beforeAll(async () => {
    app = await buildApp();
  });

  afterAll(async () => {
    await app.close();
  });

  it('deve responder 200 OK no health check público e na raiz', async () => {
    const response = await app.inject({
      method: 'GET',
      url: '/health'
    });

    expect(response.statusCode).toBe(200);
    const body = JSON.parse(response.payload);
    expect(body.status).toBe('UP');
    expect(body.service).toBe('nexuspay-edge-gateway');

    const rootRes = await app.inject({
      method: 'GET',
      url: '/'
    });
    expect(rootRes.statusCode).toBe(200);
  });

  it('deve retornar 401 Unauthorized para rotas protegidas sem header Authorization ou token inválido', async () => {
    const response = await app.inject({
      method: 'POST',
      url: '/api/v1/transacoes',
      payload: {
        lojistaId: 'lojista_123',
        valor: 100.00
      }
    });
    expect(response.statusCode).toBe(401);

    const invalidAuthRes = await app.inject({
      method: 'POST',
      url: '/api/v1/transacoes',
      headers: { authorization: 'Basic 123' },
      payload: { lojistaId: 'lojista_123' }
    });
    expect(invalidAuthRes.statusCode).toBe(401);
  });

  it('deve rotear transações com sucesso quando backend responde e tratar erro de rede', async () => {
    const originalFetch = global.fetch;
    
    // 1. Success case
    global.fetch = jest.fn().mockResolvedValue({
      status: 201,
      ok: true,
      json: async () => ({ id: 'tx-123', status: 'AUTORIZADO' })
    } as any);

    const response = await app.inject({
      method: 'POST',
      url: '/api/v1/transacoes',
      headers: {
        authorization: 'Bearer mock-jwt-token-for-dev'
      },
      payload: {
        lojistaId: 'lojista_123',
        valor: 100.00
      }
    });

    expect(response.statusCode).toBe(201);
    expect(JSON.parse(response.payload).id).toBe('tx-123');

    // 2. Error case
    global.fetch = jest.fn().mockRejectedValue(new Error('Connection failure to Java service'));
    const errRes = await app.inject({
      method: 'POST',
      url: '/api/v1/transacoes',
      headers: { authorization: 'Bearer mock-jwt' },
      payload: { lojistaId: 'lojista_123' }
    });
    expect(errRes.statusCode).toBe(503);

    global.fetch = originalFetch;
  });

  it('deve rotear diagnósticos de POS com sucesso e tratar erro de backend', async () => {
    const originalFetch = global.fetch;
    global.fetch = jest.fn().mockResolvedValue({
      status: 200,
      ok: true,
      json: async () => ({ status: 'RESOLVED', diagnostic: 'OK' })
    } as any);

    const response = await app.inject({
      method: 'POST',
      url: '/api/v1/diagnosis/pos',
      headers: { authorization: 'Bearer mock-jwt-token' },
      payload: { terminalId: 'term-1', errorCode: 'ERR_58' }
    });
    expect(response.statusCode).toBe(200);

    // Test error case
    global.fetch = jest.fn().mockRejectedValue(new Error('Connection error'));
    const errResponse = await app.inject({
      method: 'POST',
      url: '/api/v1/diagnosis/pos',
      headers: { authorization: 'Bearer mock-jwt-token' },
      payload: { terminalId: 'term-1' }
    });
    expect(errResponse.statusCode).toBe(503);

    global.fetch = originalFetch;
  });

  it('deve validar e processar streaming SSE no /api/v1/chat/stream', async () => {
    // 1. Validation error: missing prompt
    const badReq = await app.inject({
      method: 'POST',
      url: '/api/v1/chat/stream',
      headers: { authorization: 'Bearer mock-jwt' },
      payload: { lojistaId: 'loj-1' }
    });
    expect(badReq.statusCode).toBe(400);

    // 2. Successful SSE Streaming with reader chunks
    const originalFetch = global.fetch;
    const encoder = new TextEncoder();
    const chunks = [encoder.encode('data: {"token": "Olá"}\n\n')];
    let chunkIndex = 0;

    const mockBody = {
      getReader: () => ({
        read: async () => {
          if (chunkIndex < chunks.length) {
            return { done: false, value: chunks[chunkIndex++] };
          }
          return { done: true, value: undefined };
        }
      })
    };

    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      body: mockBody
    } as any);

    const sseResponse = await app.inject({
      method: 'POST',
      url: '/api/v1/chat/stream',
      headers: { authorization: 'Bearer mock-jwt' },
      payload: { lojistaId: 'loj-1', prompt: 'Qual é a taxa?' }
    });
    expect(sseResponse.statusCode).toBe(200);
    expect(sseResponse.payload).toContain('data: {"token": "Olá"}');

    // 3. Error case in SSE stream
    global.fetch = jest.fn().mockRejectedValue(new Error('SSE connection failed'));
    const sseErrResponse = await app.inject({
      method: 'POST',
      url: '/api/v1/chat/stream',
      headers: { authorization: 'Bearer mock-jwt' },
      payload: { lojistaId: 'loj-1', prompt: 'Erro de teste' }
    });
    expect(sseErrResponse.payload).toContain('Erro de comunicação interna');

    // 4. Copilot response not ok
    global.fetch = jest.fn().mockResolvedValue({
      ok: false,
      body: null
    } as any);
    const sseNotOkResponse = await app.inject({
      method: 'POST',
      url: '/api/v1/chat/stream',
      headers: { authorization: 'Bearer mock-jwt' },
      payload: { lojistaId: 'loj-1', prompt: 'Erro status' }
    });
    expect(sseNotOkResponse.payload).toContain('Falha ao conectar com o Copilot RAG Service');

    global.fetch = originalFetch;
  });
});
