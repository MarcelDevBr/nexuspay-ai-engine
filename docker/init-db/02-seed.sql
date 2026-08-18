-- =============================================================================
-- NexusPay AI Engine - Seed Data
-- =============================================================================

-- Lojistas de Teste
INSERT INTO lojistas (id, razao_social, cnpj_hash, email_contato, status)
VALUES 
    ('lojista_123', 'Supermercado Silva & Filhos Ltda', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'contato@supermercadossilva.com.br', 'ATIVO'),
    ('lojista_456', 'Restaurante Sabor Mineiro EIRELI', 'f2ca1bb6c7e907d06dafe4687e579fce76b37e4e93b7605022da52e6ccc26fd2', 'financeiro@sabormineiro.com.br', 'ATIVO')
ON CONFLICT (id) DO NOTHING;

-- Transações Financeiras Iniciais
INSERT INTO transacoes (id, lojista_id, terminal_id, valor, tipo, status, codigo_autorizacao, criado_em)
VALUES 
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'lojista_123', 'POS_STONE_9876', 450.00, 'CREDITO_A_VISTA', 'LIQUIDADA', 'AUTH_987654', NOW() - INTERVAL '1 day'),
    ('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', 'lojista_123', 'POS_STONE_9876', 1250.00, 'CREDITO_PARCELADO', 'AUTORIZADA', 'AUTH_112233', NOW() - INTERVAL '2 hours'),
    ('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a33', 'lojista_123', 'POS_STONE_9876', 85.50, 'PIX', 'LIQUIDADA', 'PIX_778899', NOW() - INTERVAL '30 minutes')
ON CONFLICT DO NOTHING;

-- Base de Conhecimento RAG (Políticas, Taxas de Antecipação, Resolução POS e BACEN)
-- Embedding dummy de 1536 dimensões com vetor unitário para testes locais
INSERT INTO documentos_conhecimento (id, titulo, categoria, conteudo, metadados, embedding)
VALUES 
    (
        'd0eebc99-9c0b-4ef8-bb6d-6bb9bd380d01',
        'Taxas de Antecipação Automática de Recebíveis',
        'TAXAS',
        'A taxa de antecipação automática para vendas no crédito à vista é de 1.99% ao mês para lojistas do segmento alimentício. Para o lojista Supermercado Silva (ID lojista_123), o desconto de R$ 45,00 em 17/08/2026 refere-se à antecipação contratual de recebíveis do lote de vendas com prazo original de 30 dias.',
        '{"modulo": "copilot", "versao": "2026.1", "topico": "antecipacao"}',
        array_fill(0.0256, ARRAY[1536])::vector
    ),
    (
        'd0eebc99-9c0b-4ef8-bb6d-6bb9bd380d02',
        'Procedimento de Reset de Chaves de Segurança POS Stone',
        'MAQUININHAS',
        'Quando a maquininha apresentar Erro 58 ou Falha de Criptografia EMV/PINPAD, execute a função reset_pos_security_keys. O terminal reiniciará em modo de manutenção e fará novo download das chaves Master/Session via canal TLS 1.3 seguro.',
        '{"modulo": "diagnostico", "codigo_erro": "ERR_58"}',
        array_fill(0.0128, ARRAY[1536])::vector
    ),
    (
        'd0eebc99-9c0b-4ef8-bb6d-6bb9bd380d03',
        'Regras de Disputa e Defesa de Chargeback BACEN e Visa/Mastercard',
        'CHARGEBACK_COMPLIANCE',
        'Para contestações com motivo "Fraude Amigável" ou "Não Reconhecimento de Compra", comprovantes impressos com captura de chip EMV e senha pessoal física possuem presunção de legitimidade (Liability Shift). O dossiê de defesa deve anexar log de autorização ISO8583 e geolocalização do terminal.',
        '{"modulo": "disputas", "normativa": "BACEN_Resolucao_150"}',
        array_fill(0.0195, ARRAY[1536])::vector
    )
ON CONFLICT DO NOTHING;
