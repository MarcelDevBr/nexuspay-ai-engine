package com.nexuspay.infrastructure.controllers;

import com.nexuspay.application.service.TransacaoService;
import com.nexuspay.domain.model.StatusTransacao;
import com.nexuspay.domain.model.TipoTransacao;
import com.nexuspay.infrastructure.controllers.dto.TransacaoRequest;
import com.nexuspay.infrastructure.controllers.dto.TransacaoResponse;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

class TransacaoControllerTest {

    private TransacaoService transacaoService;
    private TransacaoController controller;

    @BeforeEach
    void setUp() {
        transacaoService = Mockito.mock(TransacaoService.class);
        controller = new TransacaoController(transacaoService);
    }

    @Test
    void testAutorizarTransacaoSuccess() {
        TransacaoRequest req = new TransacaoRequest("loj_1", "term_1", new BigDecimal("100.00"), TipoTransacao.CREDITO_A_VISTA);
        TransacaoResponse mockResp = new TransacaoResponse(
                UUID.randomUUID(),
                "loj_1",
                "term_1",
                new BigDecimal("100.00"),
                TipoTransacao.CREDITO_A_VISTA,
                StatusTransacao.AUTORIZADA,
                "AUTH_123",
                OffsetDateTime.now(),
                "Autorizada"
        );

        when(transacaoService.processarTransacao(any())).thenReturn(mockResp);

        ResponseEntity<TransacaoResponse> responseEntity = controller.autorizarTransacao(req);
        assertEquals(HttpStatus.CREATED, responseEntity.getStatusCode());
        assertNotNull(responseEntity.getBody());
        assertEquals("loj_1", responseEntity.getBody().getLojistaId());
    }
}
