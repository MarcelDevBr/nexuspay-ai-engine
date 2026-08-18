package com.nexuspay.domain.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.OffsetDateTime;

@Entity
@Table(name = "lojistas")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Lojista {

    @Id
    @Column(length = 50)
    private String id;

    @Column(name = "razao_social", nullable = false)
    private String razaoSocial;

    @Column(name = "cnpj_hash", nullable = false, unique = true, length = 64)
    private String cnpjHash;

    @Column(name = "email_contato", nullable = false, length = 150)
    private String emailContato;

    @Column(nullable = false, length = 20)
    private String status;

    @Column(name = "criado_em")
    private OffsetDateTime criadoEm;
}
