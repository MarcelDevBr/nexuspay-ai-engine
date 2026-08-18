package com.nexuspay.domain.model;

import org.junit.jupiter.api.Test;
import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class TransacaoTest {

    @Test
    void testTransacaoGettersAndSetters() {
        UUID id = UUID.randomUUID();
        OffsetDateTime now = OffsetDateTime.now();
        TransacaoId transacaoId = new TransacaoId(id, now);

        Transacao tx = new Transacao();
        tx.setId(transacaoId);
        tx.setLojistaId("lojista_123");
        tx.setTerminalId("term_01");
        tx.setValor(new BigDecimal("150.50"));
        tx.setTipo(TipoTransacao.CREDITO_A_VISTA);
        tx.setStatus(StatusTransacao.AUTORIZADA);
        tx.setCodigoAutorizacao("AUTH_12345");

        assertEquals(transacaoId, tx.getId());
        assertEquals("lojista_123", tx.getLojistaId());
        assertEquals("term_01", tx.getTerminalId());
        assertEquals(new BigDecimal("150.50"), tx.getValor());
        assertEquals(TipoTransacao.CREDITO_A_VISTA, tx.getTipo());
        assertEquals(StatusTransacao.AUTORIZADA, tx.getStatus());
        assertEquals("AUTH_12345", tx.getCodigoAutorizacao());
    }

    @Test
    void testTransacaoAllArgsConstructor() {
        TransacaoId transacaoId = new TransacaoId(UUID.randomUUID(), OffsetDateTime.now());
        Transacao tx = new Transacao(
                transacaoId,
                "loj_999",
                "term_99",
                BigDecimal.TEN,
                TipoTransacao.PIX,
                StatusTransacao.AUTORIZADA,
                "AUTH_PIX"
        );

        assertNotNull(tx);
        assertEquals("loj_999", tx.getLojistaId());
        assertEquals(TipoTransacao.PIX, tx.getTipo());
    }
}
