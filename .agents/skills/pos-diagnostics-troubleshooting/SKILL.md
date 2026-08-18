---
name: pos-diagnostics-troubleshooting
description: >-
  Diagnóstico de maquininhas de cartão POS e telemetria. Use para compreender erros ISO 8583,
  falhas de sincronismo de chaves criptográficas EMV/PINPAD (ERR_58) e Function Calling determinístico.
---

# POS Diagnostics Troubleshooting Skill

## Protocolos Suportados

- **`ERR_58` / Falha de Criptografia:** Executa `reset_pos_security_keys` via canal seguro TLS.
- **`ERR_45` / Leitor de Chip:** Executa calibração e limpeza remota de sensor EMV.
- **`ERR_91` / Timeout de Conectividade:** Reinicia canal de telemetria 4G/Wi-Fi.
