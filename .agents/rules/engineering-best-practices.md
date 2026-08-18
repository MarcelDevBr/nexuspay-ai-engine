---
trigger: always_on
---

# 🌟 Melhores Práticas de Engenharia de Software no NexusPay

1. **Tipagem Estrita & Modelagem Imutável:**
   - **TypeScript:** Habilite e respeite o modo `strict`, evite o uso de `any` e declare interfaces explícitas para requisições e respostas.
   - **Java:** Utilize `record`, `@Builder`, `@Value` (Lombok) e imutabilidade sempre que possível para DTOs e eventos.
   - **Python:** Use **Pydantic v2** com anotações de tipo completas (`typing`, `Optional`, `List`, `Dict`) e `pydantic-settings` para configurações.

2. **Tratamento Resiliente de Erros & Fail-Safe:**
   - Nunca capture e silencie exceções com blocos vazios (`except: pass` é estritamente proibido).
   - Registre logs contextuais informando causa, ID da transação (`transacao_id`) e lojista (`lojista_id`).
   - Retorne códigos de status HTTP semânticos (400, 401, 403, 404, 422, 500, 503) e contratos de erro padronizados.

3. **Nomenclatura Limpa & Código Autoexplicativo (Clean Code):**
   - Use nomes de variáveis, métodos e classes que revelem sua intenção de negócio de forma clara, sem abreviações obscuras.
   - Funções devem ser pequenas, focadas e executar apenas uma única responsabilidade.

4. **Segurança por Padrão (Security by Design & PCI-DSS):**
   - Sanitização de dados sensíveis (números de cartão PAN, CVV, senhas e CPFs) antes de qualquer persistência ou log.
   - NUNCA versione credenciais, tokens de API ou senhas em texto plano.

5. **Observabilidade & Logs Estruturados:**
   - Utilize loggers formais (`logging` no Python, `SLF4J`/`Logback` no Java, `fastify.log` no Node.js) em vez de `print()` ou `console.log()`.
   - Adicione logs estruturados com níveis apropriados (`DEBUG`, `INFO`, `WARNING`, `ERROR`).

6. **Twelve-Factor App & Governança de Configurações:**
   - Isole configurações em variáveis de ambiente tipadas e validadas no momento da inicialização da aplicação.
   - Garanta paridade total entre ambientes de desenvolvimento (LocalStack/Docker) e produção (AWS EKS).

7. **Princípio KISS (Keep It Simple, Stupid!):**
   - Prefira soluções simples, elegantes e diretas em vez de abstrações desnecessárias, padrões rebuscados sem justificativa real e sobre-engenharia (*over-engineering*).
   - O design mais eficiente é aquele que resolve o problema de negócio com o menor número de camadas e com a maior legibilidade possível.

