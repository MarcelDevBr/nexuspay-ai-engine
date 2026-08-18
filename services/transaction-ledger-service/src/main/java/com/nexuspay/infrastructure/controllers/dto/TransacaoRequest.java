package com.nexuspay.infrastructure.controllers.dto;

import com.nexuspay.domain.model.TipoTransacao;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.math.BigDecimal;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TransacaoRequest {

    @NotBlank(message = "lojista_id é obrigatório")
    private String lojistaId;

    private String terminalId;

    @NotNull(message = "valor é obrigatório")
    @DecimalMin(value = "0.01", message = "O valor deve ser maior que zero")
    private BigDecimal valor;

    @NotNull(message = "tipo é obrigatório")
    private TipoTransacao tipo;

    public TransacaoRequest() {}

    public TransacaoRequest(String lojistaId, String terminalId, BigDecimal valor, TipoTransacao tipo) {
        this.lojistaId = lojistaId;
        this.terminalId = terminalId;
        this.valor = valor;
        this.tipo = tipo;
    }

    public String getLojistaId() { return lojistaId; }
    public void setLojistaId(String lojistaId) { this.lojistaId = lojistaId; }

    public String getTerminalId() { return terminalId; }
    public void setTerminalId(String terminalId) { this.terminalId = terminalId; }

    public BigDecimal getValor() { return valor; }
    public void setValor(BigDecimal valor) { this.valor = valor; }

    public TipoTransacao getTipo() { return tipo; }
    public void setTipo(TipoTransacao tipo) { this.tipo = tipo; }
}
