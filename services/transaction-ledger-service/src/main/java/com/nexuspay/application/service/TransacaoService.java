package com.nexuspay.application.service;

import com.nexuspay.domain.model.*;
import com.nexuspay.infrastructure.controllers.dto.TransacaoRequest;
import com.nexuspay.infrastructure.controllers.dto.TransacaoResponse;
import com.nexuspay.infrastructure.persistence.LojistaRepository;
import com.nexuspay.infrastructure.persistence.OutboxEventRepository;
import com.nexuspay.infrastructure.persistence.TransacaoRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.OffsetDateTime;
import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class TransacaoService {

    private static final Logger logFallback = LoggerFactory.getLogger(TransacaoService.class);

    private final TransacaoRepository transacaoRepository;
    private final LojistaRepository lojistaRepository;
    private final OutboxEventRepository outboxEventRepository;

    public TransacaoService(TransacaoRepository transacaoRepository, LojistaRepository lojistaRepository, OutboxEventRepository outboxEventRepository) {
        this.transacaoRepository = transacaoRepository;
        this.lojistaRepository = lojistaRepository;
        this.outboxEventRepository = outboxEventRepository;
    }

    @Transactional
    public TransacaoResponse processarTransacao(TransacaoRequest request) {
        logFallback.info("Iniciando autorização de transação para lojista: {}", request.getLojistaId());

        lojistaRepository.findById(request.getLojistaId())
                .orElseThrow(() -> new IllegalArgumentException("Lojista não encontrado: " + request.getLojistaId()));

        UUID transacaoUuid = UUID.randomUUID();
        OffsetDateTime agora = OffsetDateTime.now();
        String codigoAutorizacao = "AUTH_" + System.currentTimeMillis();

        Transacao transacao = new Transacao(
                new TransacaoId(transacaoUuid, agora),
                request.getLojistaId(),
                request.getTerminalId(),
                request.getValor(),
                request.getTipo(),
                StatusTransacao.AUTORIZADA,
                codigoAutorizacao
        );

        transacaoRepository.save(transacao);

        String payloadJson = String.format(
                "{\"transacaoId\":\"%s\",\"lojistaId\":\"%s\",\"valor\":%s,\"tipo\":\"%s\",\"codigoAutorizacao\":\"%s\",\"criadoEm\":\"%s\"}",
                transacaoUuid, request.getLojistaId(), request.getValor(), request.getTipo(), codigoAutorizacao, agora
        );

        OutboxEvent outboxEvent = new OutboxEvent("TRANSACAO", transacaoUuid.toString(), "TransacaoAutorizadaEvent", payloadJson);
        outboxEvent.setCriadoEm(agora);

        outboxEventRepository.save(outboxEvent);

        logFallback.info("Transação autorizada com sucesso! ID: {}, Código: {}", transacaoUuid, codigoAutorizacao);

        return new TransacaoResponse(
                transacaoUuid,
                request.getLojistaId(),
                request.getTerminalId(),
                request.getValor(),
                request.getTipo(),
                StatusTransacao.AUTORIZADA,
                codigoAutorizacao,
                agora,
                "Transação autorizada com sucesso."
        );
    }
}
