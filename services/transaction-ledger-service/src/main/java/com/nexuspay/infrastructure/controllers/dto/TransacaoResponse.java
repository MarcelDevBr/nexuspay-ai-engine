package com.nexuspay.infrastructure.controllers.dto;

import com.nexuspay.domain.model.StatusTransacao;
import com.nexuspay.domain.model.TipoTransacao;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.UUID;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TransacaoResponse {
    private UUID id;
    private String lojistaId;
    private String terminalId;
    private BigDecimal valor;
    private TipoTransacao tipo;
    private StatusTransacao status;
    private String codigoAutorizacao;
    private OffsetDateTime criadoEm;
    private String mensagem;
}
