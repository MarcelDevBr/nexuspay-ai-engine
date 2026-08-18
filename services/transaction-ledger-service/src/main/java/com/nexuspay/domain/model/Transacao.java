package com.nexuspay.domain.model;

import jakarta.persistence.*;
import java.math.BigDecimal;

@Entity
@Table(name = "transacoes")
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

    public Transacao() {}

    public Transacao(TransacaoId id, String lojistaId, String terminalId, BigDecimal valor, TipoTransacao tipo, StatusTransacao status, String codigoAutorizacao) {
        this.id = id;
        this.lojistaId = lojistaId;
        this.terminalId = terminalId;
        this.valor = valor;
        this.tipo = tipo;
        this.status = status;
        this.codigoAutorizacao = codigoAutorizacao;
    }

    public TransacaoId getId() { return id; }
    public void setId(TransacaoId id) { this.id = id; }

    public String getLojistaId() { return lojistaId; }
    public void setLojistaId(String lojistaId) { this.lojistaId = lojistaId; }

    public String getTerminalId() { return terminalId; }
    public void setTerminalId(String terminalId) { this.terminalId = terminalId; }

    public BigDecimal getValor() { return valor; }
    public void setValor(BigDecimal valor) { this.valor = valor; }

    public TipoTransacao getTipo() { return tipo; }
    public void setTipo(TipoTransacao tipo) { this.tipo = tipo; }

    public StatusTransacao getStatus() { return status; }
    public void setStatus(StatusTransacao status) { this.status = status; }

    public String getCodigoAutorizacao() { return codigoAutorizacao; }
    public void setCodigoAutorizacao(String codigoAutorizacao) { this.codigoAutorizacao = codigoAutorizacao; }
}
