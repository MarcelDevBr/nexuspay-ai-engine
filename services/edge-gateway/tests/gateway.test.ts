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

  it('deve responder 200 OK no health check público', async () => {
    const response = await app.inject({
      method: 'GET',
      url: '/health'
    });

    expect(response.statusCode).toBe(200);
    const body = JSON.parse(response.payload);
    expect(body.status).toBe('UP');
    expect(body.service).toBe('nexuspay-edge-gateway');
  });

  it('deve retornar 401 Unauthorized para rotas protegidas sem header Authorization', async () => {
    const response = await app.inject({
      method: 'POST',
      url: '/api/v1/transacoes',
      payload: {
        lojistaId: 'lojista_123',
        valor: 100.00
      }
    });

    expect(response.statusCode).toBe(401);
  });

  it('deve aceitar requisição com Bearer Token simulado', async () => {
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

    // Como o backend alvo mock não está rodando no teste unitário, o proxy responde ou passa
    expect([200, 502, 503]).toContain(response.statusCode);
  });
});
