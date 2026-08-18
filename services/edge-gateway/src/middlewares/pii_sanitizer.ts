/**
 * PII Sanitizer & PCI-DSS Guardrails Middleware
 * Mascara dados sensíveis (Cartão PAN, CPF, CVV) em payloads de entrada antes de encaminhar para a IA.
 */

const CREDIT_CARD_REGEX = /\b(?:\d[ -]*?){13,19}\b/g;
const CPF_REGEX = /\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b/g;
const CVV_REGEX = /(?:cvv|cvc|código de segurança)[:\s]*([0-9]{3,4})/gi;

export function maskCreditCard(text: string): string {
  return text.replace(CREDIT_CARD_REGEX, (match) => {
    const clean = match.replace(/[\s-]/g, '');
    if (clean.length >= 13 && clean.length <= 19) {
      const last4 = clean.slice(-4);
      return `[CARD_FINAL_${last4}]`;
    }
    return match;
  });
}

export function maskCPF(text: string): string {
  return text.replace(CPF_REGEX, () => '[CPF_PROTEGIDO]');
}

export function maskCVV(text: string): string {
  return text.replace(CVV_REGEX, 'cvv: [REDACTED]');
}

export function sanitizePayload(payload: any): any {
  if (typeof payload === 'string') {
    let sanitized = maskCreditCard(payload);
    sanitized = maskCPF(sanitized);
    sanitized = maskCVV(sanitized);
    return sanitized;
  }

  if (Array.isArray(payload)) {
    return payload.map(item => sanitizePayload(item));
  }

  if (payload !== null && typeof payload === 'object') {
    const sanitizedObj: Record<string, any> = {};
    for (const key of Object.keys(payload)) {
      if (['cvv', 'cvc', 'security_code', 'password', 'senha'].includes(key.toLowerCase())) {
        sanitizedObj[key] = '[REDACTED]';
      } else {
        sanitizedObj[key] = sanitizePayload(payload[key]);
      }
    }
    return sanitizedObj;
  }

  return payload;
}
