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
}
