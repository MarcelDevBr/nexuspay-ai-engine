package com.nexuspay.domain.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.OffsetDateTime;

@Entity
@Table(name = "lojistas")
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

    public Lojista() {}

    public Lojista(String id, String razaoSocial, String cnpjHash, String emailContato, String status, OffsetDateTime criadoEm) {
        this.id = id;
        this.razaoSocial = razaoSocial;
        this.cnpjHash = cnpjHash;
        this.emailContato = emailContato;
        this.status = status;
        this.criadoEm = criadoEm;
    }

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getRazaoSocial() { return razaoSocial; }
    public void setRazaoSocial(String razaoSocial) { this.razaoSocial = razaoSocial; }

    public String getCnpjHash() { return cnpjHash; }
    public void setCnpjHash(String cnpjHash) { this.cnpjHash = cnpjHash; }

    public String getEmailContato() { return emailContato; }
    public void setEmailContato(String emailContato) { this.emailContato = emailContato; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public OffsetDateTime getCriadoEm() { return criadoEm; }
    public void setCriadoEm(OffsetDateTime criadoEm) { this.criadoEm = criadoEm; }
}
