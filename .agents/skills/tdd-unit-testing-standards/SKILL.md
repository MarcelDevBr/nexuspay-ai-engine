---
name: tdd-unit-testing-standards
description: >-
  Diretrizes e fluxos de Test-Driven Development (TDD) e padrões de testes unitários 1:1. Use
  ao criar, refatorar ou testar qualquer módulo, serviço ou componente no NexusPay AI Engine,
  garantindo paridade exata de nomes de arquivo e 100% de cobertura.
---

# TDD & Padrões de Testes Unitários 1:1

## 📌 Regras de Ouro
1. **Desenvolvimento Orientado a Testes (TDD):**
   * **Red:** Crie o teste unitário que define o comportamento esperado antes de escrever a lógica.
   * **Green:** Escreva a implementação mínima para fazer o teste passar.
   * **Refactor:** Limpe e otimize o código mantendo o teste verde e 100% de cobertura.

2. **Paridade 1:1 de Arquivos e Nomenclatura:**
   * Todo arquivo de código deve ter um arquivo de teste dedicado com o mesmo nome e sufixo de teste no final.
   * **Python:** `src/foo/bar.py` ➔ `tests/foo/test_bar.py` ou `tests/foo/bar_test.py`.
   * **TypeScript/Node.js:** `src/foo/bar.ts` ➔ `tests/foo/bar.test.ts`.
   * **Java:** `src/main/java/.../Bar.java` ➔ `src/test/java/.../BarTest.java`.

3. **100% de Cobertura de Código:**
   * Todas as branches condicionais, exceções, fallbacks e funções devem ter asserções explícitas.

4. **Princípio DRY (Don't Repeat Yourself):**
   * Elimine rigorosamente duplicações de código tanto na aplicação quanto nos testes.
   * Centralize fixtures, mock data builders, helpers e utilitários compartilhados para garantir facilidade de manutenção e clareza.

5. **Princípio KISS (Keep It Simple, Stupid!):**
   * Na etapa **Green**, escreva a solução mais simples possível para fazer o teste passar.
   * Na etapa **Refactor**, simplifique o design e evite abstrações desnecessárias antes de haver necessidade comprovada.


