---
trigger: always_on
---

# 🧪 Diretrizes de Testes Unitários e TDD no NexusPay

1. **Preceitos do Test-Driven Development (TDD):**
   - Todo desenvolvimento ou modificação de funcionalidade deve seguir rigorosamente o ciclo **Red -> Green -> Refactor**.
   - Escreva o teste antes da implementação, faça-o passar com a implementação mínima necessária e refatore mantendo 100% de cobertura.

2. **Relação Direta 1:1 de Arquivos e Testes:**
   - Cada arquivo de código-fonte (`src/`) deve possuir obrigatoriamente um arquivo de teste correspondente na proporção estrita de **1:1**.
   - É proibido agrupar múltiplos módulos em um único arquivo de teste genérico.

3. **Convenção Estrita de Nomenclatura dos Arquivos de Teste:**
   - O arquivo de teste deve ter **exatamente o mesmo nome** do arquivo de código-fonte de origem, com o sufixo `test` ou `_test` no final do nome do arquivo antes da extensão:
     - **Python (Python 3.14):** `src/services/rag_service.py` -> `tests/services/rag_service_test.py` (ou `tests/test_rag_service.py` mantendo o nome exato do módulo).
     - **TypeScript/Node.js (Node.js 26):** `src/routes/proxy.ts` -> `tests/routes/proxy.test.ts`.
     - **Java (Java 26 / Spring Boot 4):** `src/main/java/.../TransacaoService.java` -> `src/test/java/.../TransacaoServiceTest.java`.

4. **100% de Cobertura de Código Obrigatória:**
   - Todos os arquivos de teste devem cobrir 100% das linhas, funções, branches condicionais e fluxos de exceção/fallback do seu arquivo correspondente.
   - Nenhuma nova funcionalidade ou refatoração pode ser aceita com cobertura inferior a 100%.

5. **Princípio DRY (Don't Repeat Yourself) & Eliminação de Código Duplicado:**
   - Evite sempre que possível a duplicação de código fonte e de código de testes.
   - Reaproveite fixtures, factories de dados de teste, helpers e mocks centralizados.
   - Refatore testes redundantes e código de produção duplicado para funções ou módulos utilitários coesos durante a etapa **Refactor** do TDD.

