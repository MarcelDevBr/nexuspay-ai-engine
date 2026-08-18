---
trigger: always_on
---

# 📐 Diretrizes de Arquitetura Limpa, SOLID e Clean Code no NexusPay

1. **Single Responsibility Principle (SRP):** Cada classe, módulo ou handler deve ter uma única razão para mudar. Não misture regras de domínio com detalhes de framework.
2. **Open/Closed Principle (OCP):** Use interfaces e o Strategy Pattern para estender comportamentos (como em diagnósticos de POS e agentes de disputas) sem alterar o código existente.
3. **Liskov Substitution Principle (LSP):** Todas as implementações de interfaces (Ports) devem ser perfeitamente intercambiáveis sem alterar a corretude do sistema.
4. **Interface Segregation Principle (ISP):** Crie interfaces pequenas e específicas para cada papel de agente ou serviço.
5. **Dependency Inversion Principle (DIP):** Dependa de abstrações/interfaces (Ports), nunca de implementações concretas (Adapters).
6. **Zero Hardcoded Secrets & FinOps:** Nunca adicione chaves de API estáticas. Sempre mantenha o fallback mock ativo para testes locais e garanta custo zero na nuvem.
7. **TDD & Testes Unitários 1:1:** Siga rigorosamente o ciclo TDD (Red-Green-Refactor). Cada arquivo de código fonte deve ter um arquivo de teste diretamente relacionado na proporção de 1:1, com o mesmo nome acrescido do sufixo `test` no final (ex.: `servico.py` -> `servico_test.py`, `Servico.java` -> `ServicoTest.java`, `servico.ts` -> `servico.test.ts`), garantindo 100% de cobertura.
8. **Princípio DRY (Don't Repeat Yourself) & Eliminação de Código Duplicado:** Evite rigorosamente a duplicação de código e lógica em todos os microsserviços. Extraia comportamentos reutilizáveis em funções utilitárias, componentes de infraestrutura compartilhados, decorators/middlewares ou classes base, mantendo o código limpo, coeso e de fácil manutenção.
9. **Boas Práticas de Engenharia de Software & Clean Code:** Adote tipagem estrita (TypeScript/Pydantic/Java Records), logs estruturados e contextuais (sem `print` ou `console.log`), tratamento resiliente de erros com códigos HTTP semânticos, segurança por design (PCI-DSS) e isolamento de configurações (Twelve-Factor App).
10. **Princípio KISS (Keep It Simple, Stupid!):** Priorize a simplicidade, clareza e legibilidade. Evite complexidade desnecessária, abstrações prematuras e *over-engineering*. Escreva o código mais direto, compreensível e fácil de testar para resolver o problema de negócio.



