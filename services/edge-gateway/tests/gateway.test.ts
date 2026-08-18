import { sanitizePayload, maskCreditCard, maskCPF, maskCVV } from '../src/middlewares/pii_sanitizer';

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
