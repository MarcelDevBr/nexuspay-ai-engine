package com.nexuspay.domain.model;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.io.Serializable;
import java.time.OffsetDateTime;
import java.util.Objects;
import java.util.UUID;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Embeddable
public class TransacaoId implements Serializable {

    @Column(name = "id")
    private UUID id;

    @Column(name = "criado_em")
    private OffsetDateTime criadoEm;

    public TransacaoId() {}

    public TransacaoId(UUID id, OffsetDateTime criadoEm) {
        this.id = id;
        this.criadoEm = criadoEm;
    }

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public OffsetDateTime getCriadoEm() { return criadoEm; }
    public void setCriadoEm(OffsetDateTime criadoEm) { this.criadoEm = criadoEm; }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        TransacaoId that = (TransacaoId) o;
        return Objects.equals(id, that.id) && Objects.equals(criadoEm, that.criadoEm);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, criadoEm);
    }
}
