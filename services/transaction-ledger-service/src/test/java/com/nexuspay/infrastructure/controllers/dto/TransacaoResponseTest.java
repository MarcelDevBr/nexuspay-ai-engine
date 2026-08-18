package com.nexuspay.infrastructure.controllers.dto;

import com.nexuspay.domain.model.StatusTransacao;
import com.nexuspay.domain.model.TipoTransacao;
import org.junit.jupiter.api.Test;
import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class TransacaoResponseTest {

    @Test
    void testGettersAndSetters() {
        UUID id = UUID.randomUUID();
        OffsetDateTime now = OffsetDateTime.now();

        TransacaoResponse res = new TransacaoResponse();
        res.setId(id);
        res.setLojistaId("loj_1");
        res.setTerminalId("term_1");
        res.setValor(new BigDecimal("50.00"));
        res.setTipo(TipoTransacao.CREDITO_A_VISTA);
        res.setStatus(StatusTransacao.AUTORIZADA);
        res.setCodigoAutorizacao("AUTH_001");
        res.setCriadoEm(now);
        res.setMensagem("Sucesso");

        assertEquals(id, res.getId());
        assertEquals("loj_1", res.getLojistaId());
        assertEquals("term_1", res.getTerminalId());
        assertEquals(new BigDecimal("50.00"), res.getValor());
        assertEquals(TipoTransacao.CREDITO_A_VISTA, res.getTipo());
        assertEquals(StatusTransacao.AUTORIZADA, res.getStatus());
        assertEquals("AUTH_001", res.getCodigoAutorizacao());
        assertEquals(now, res.getCriadoEm());
        assertEquals("Sucesso", res.getMensagem());
    }

    @Test
    void testConstructor() {
        UUID id = UUID.randomUUID();
        OffsetDateTime now = OffsetDateTime.now();
        TransacaoResponse res = new TransacaoResponse(
                id,
                "loj_2",
                "term_2",
                BigDecimal.TEN,
                TipoTransacao.DEBITO,
                StatusTransacao.NEGADA,
                "AUTH_NEG",
                now,
                "Negada"
        );

        assertNotNull(res);
        assertEquals(StatusTransacao.NEGADA, res.getStatus());
    }
}
