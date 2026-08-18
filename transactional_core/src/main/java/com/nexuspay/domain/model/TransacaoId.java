package com.nexuspay.domain.model;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;
import java.time.OffsetDateTime;
import java.util.UUID;

@Embeddable
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TransacaoId implements Serializable {

    @Column(name = "id")
    private UUID id;

    @Column(name = "criado_em")
    private OffsetDateTime criadoEm;
}
