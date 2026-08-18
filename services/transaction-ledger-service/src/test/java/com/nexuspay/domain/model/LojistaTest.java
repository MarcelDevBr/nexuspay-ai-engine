package com.nexuspay.domain.model;

import org.junit.jupiter.api.Test;
import java.time.OffsetDateTime;

import static org.junit.jupiter.api.Assertions.*;

class LojistaTest {

    @Test
    void testLojistaGettersAndSetters() {
        OffsetDateTime now = OffsetDateTime.now();
        Lojista lojista = new Lojista();
        lojista.setId("lojista_123");
        lojista.setRazaoSocial("Padaria Central LTDA");
        lojista.setCnpjHash("hash_cnpj_12345");
        lojista.setEmailContato("contato@padaria.com.br");
        lojista.setStatus("ATIVO");
        lojista.setCriadoEm(now);

        assertEquals("lojista_123", lojista.getId());
        assertEquals("Padaria Central LTDA", lojista.getRazaoSocial());
        assertEquals("hash_cnpj_12345", lojista.getCnpjHash());
        assertEquals("contato@padaria.com.br", lojista.getEmailContato());
        assertEquals("ATIVO", lojista.getStatus());
        assertEquals(now, lojista.getCriadoEm());
    }

    @Test
    void testLojistaAllArgsConstructor() {
        OffsetDateTime now = OffsetDateTime.now();
        Lojista lojista = new Lojista(
                "lojista_456",
                "Supermercado Top",
                "hash_top",
                "admin@top.com",
                "ATIVO",
                now
        );

        assertNotNull(lojista);
        assertEquals("Supermercado Top", lojista.getRazaoSocial());
    }
}
