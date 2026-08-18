package com.nexuspay.domain.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;

@Entity
@Table(name = "transacoes")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Transacao {

    @EmbeddedId
    private TransacaoId id;

    @Column(name = "lojista_id", nullable = false, length = 50)
    private String lojistaId;

    @Column(name = "terminal_id", length = 50)
    private String terminalId;

    @Column(nullable = false, precision = 15, scale = 2)
    private BigDecimal valor;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    private TipoTransacao tipo;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private StatusTransacao status;

    @Column(name = "codigo_autorizacao", length = 50)
    private String codigoAutorizacao;
}
