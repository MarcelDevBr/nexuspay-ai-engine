package com.nexuspay.application.service;

import com.nexuspay.domain.model.Lojista;
import com.nexuspay.domain.model.StatusTransacao;
import com.nexuspay.domain.model.TipoTransacao;
import com.nexuspay.infrastructure.controllers.dto.TransacaoRequest;
import com.nexuspay.infrastructure.controllers.dto.TransacaoResponse;
import com.nexuspay.infrastructure.persistence.LojistaRepository;
import com.nexuspay.infrastructure.persistence.OutboxEventRepository;
import com.nexuspay.infrastructure.persistence.TransacaoRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class TransacaoServiceTest {

    @Mock
    private TransacaoRepository transacaoRepository;

    @Mock
    private LojistaRepository lojistaRepository;

    @Mock
    private OutboxEventRepository outboxEventRepository;

    @InjectMocks
    private TransacaoService transacaoService;

    private Lojista lojista;

    @BeforeEach
    void setUp() {
        lojista = new Lojista(
                "lojista_123",
                "Supermercado Silva",
                "cnpj_hash_mock",
                "contato@silva.com",
                "ATIVO",
                OffsetDateTime.now()
        );
    }

    @Test
    void deveAutorizarTransacaoEGravarOutboxComSucesso() {
        when(lojistaRepository.findById("lojista_123")).thenReturn(Optional.of(lojista));

        TransacaoRequest request = new TransacaoRequest(
                "lojista_123",
                "POS_123",
                new BigDecimal("150.00"),
                TipoTransacao.CREDITO_A_VISTA
        );

        TransacaoResponse response = transacaoService.processarTransacao(request);

        assertNotNull(response);
        assertNotNull(response.getId());
        assertEquals("lojista_123", response.getLojistaId());
        assertEquals(StatusTransacao.AUTORIZADA, response.getStatus());
        assertEquals(new BigDecimal("150.00"), response.getValor());

        verify(transacaoRepository, times(1)).save(any());
        verify(outboxEventRepository, times(1)).save(any());
    }

    @Test
    void deveLancarExcecaoQuandoLojistaNaoExistir() {
        when(lojistaRepository.findById("lojista_inexistente")).thenReturn(Optional.empty());

        TransacaoRequest request = new TransacaoRequest(
                "lojista_inexistente",
                null,
                new BigDecimal("100.00"),
                TipoTransacao.PIX
        );

        assertThrows(IllegalArgumentException.class, () -> transacaoService.processarTransacao(request));

        verify(transacaoRepository, never()).save(any());
        verify(outboxEventRepository, never()).save(any());
    }
}
