package com.nexuspay.application.service;

import com.nexuspay.domain.model.*;
import com.nexuspay.infrastructure.controllers.dto.TransacaoRequest;
import com.nexuspay.infrastructure.controllers.dto.TransacaoResponse;
import com.nexuspay.infrastructure.persistence.LojistaRepository;
import com.nexuspay.infrastructure.persistence.OutboxEventRepository;
import com.nexuspay.infrastructure.persistence.TransacaoRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.OffsetDateTime;
import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class TransacaoService {

    private final TransacaoRepository transacaoRepository;
    private final LojistaRepository lojistaRepository;
    private final OutboxEventRepository outboxEventRepository;

    @Transactional
    public TransacaoResponse processarTransacao(TransacaoRequest request) {
        log.info("Iniciando autorização de transação para lojista: {}", request.getLojistaId());

        // 1. Valida existência do Lojista
        lojistaRepository.findById(request.getLojistaId())
                .orElseThrow(() -> new IllegalArgumentException("Lojista não encontrado: " + request.getLojistaId()));

        UUID transacaoUuid = UUID.randomUUID();
        OffsetDateTime agora = OffsetDateTime.now();
        String codigoAutorizacao = "AUTH_" + System.currentTimeMillis();

        // 2. Cria Entidade Transação (Ledger ACID)
        Transacao transacao = Transacao.builder()
                .id(TransacaoId.builder()
                        .id(transacaoUuid)
                        .criadoEm(agora)
                        .build())
                .lojistaId(request.getLojistaId())
                .terminalId(request.getTerminalId())
                .valor(request.getValor())
                .tipo(request.getTipo())
                .status(StatusTransacao.AUTORIZADA)
                .codigoAutorizacao(codigoAutorizacao)
                .build();

        transacaoRepository.save(transacao);

        // 3. Grava no Transactional Outbox (Mesma transação local do banco de dados)
        String payloadJson = String.format(
                "{\"transacaoId\":\"%s\",\"lojistaId\":\"%s\",\"valor\":%s,\"tipo\":\"%s\",\"codigoAutorizacao\":\"%s\",\"criadoEm\":\"%s\"}",
                transacaoUuid, request.getLojistaId(), request.getValor(), request.getTipo(), codigoAutorizacao, agora
        );

        OutboxEvent outboxEvent = OutboxEvent.builder()
                .aggregateType("TRANSACAO")
                .aggregateId(transacaoUuid.toString())
                .eventType("TransacaoAutorizadaEvent")
                .payload(payloadJson)
                .status("PENDENTE")
                .tentativas(0)
                .criadoEm(agora)
                .build();

        outboxEventRepository.save(outboxEvent);

        log.info("Transação autorizada com sucesso! ID: {}, Código: {}", transacaoUuid, codigoAutorizacao);

        return TransacaoResponse.builder()
                .id(transacaoUuid)
                .lojistaId(request.getLojistaId())
                .terminalId(request.getTerminalId())
                .valor(request.getValor())
                .tipo(request.getTipo())
                .status(StatusTransacao.AUTORIZADA)
                .codigoAutorizacao(codigoAutorizacao)
                .criadoEm(agora)
                .mensagem("Transação autorizada com sucesso.")
                .build();
    }
}
