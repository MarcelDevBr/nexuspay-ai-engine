package com.nexuspay.infrastructure.controllers.dto;

import com.nexuspay.domain.model.StatusTransacao;
import com.nexuspay.domain.model.TipoTransacao;
import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.UUID;

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

    public TransacaoResponse() {}

    public TransacaoResponse(UUID id, String lojistaId, String terminalId, BigDecimal valor, TipoTransacao tipo, StatusTransacao status, String codigoAutorizacao, OffsetDateTime criadoEm, String mensagem) {
        this.id = id;
        this.lojistaId = lojistaId;
        this.terminalId = terminalId;
        this.valor = valor;
        this.tipo = tipo;
        this.status = status;
        this.codigoAutorizacao = codigoAutorizacao;
        this.criadoEm = criadoEm;
        this.mensagem = mensagem;
    }

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

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

    public OffsetDateTime getCriadoEm() { return criadoEm; }
    public void setCriadoEm(OffsetDateTime criadoEm) { this.criadoEm = criadoEm; }

    public String getMensagem() { return mensagem; }
    public void setMensagem(String mensagem) { this.mensagem = mensagem; }
}
