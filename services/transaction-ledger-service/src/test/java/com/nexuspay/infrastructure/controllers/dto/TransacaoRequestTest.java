package com.nexuspay.infrastructure.controllers.dto;

import com.nexuspay.domain.model.TipoTransacao;
import org.junit.jupiter.api.Test;
import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.*;

class TransacaoRequestTest {

    @Test
    void testGettersAndSetters() {
        TransacaoRequest req = new TransacaoRequest();
        req.setLojistaId("loj_123");
        req.setTerminalId("term_01");
        req.setValor(new BigDecimal("100.00"));
        req.setTipo(TipoTransacao.DEBITO);

        assertEquals("loj_123", req.getLojistaId());
        assertEquals("term_01", req.getTerminalId());
        assertEquals(new BigDecimal("100.00"), req.getValor());
        assertEquals(TipoTransacao.DEBITO, req.getTipo());
    }

    @Test
    void testConstructor() {
        TransacaoRequest req = new TransacaoRequest("loj_1", "term_1", BigDecimal.ONE, TipoTransacao.PIX);
        assertEquals("loj_1", req.getLojistaId());
        assertEquals(TipoTransacao.PIX, req.getTipo());
    }
}
