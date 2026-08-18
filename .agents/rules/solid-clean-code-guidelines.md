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
