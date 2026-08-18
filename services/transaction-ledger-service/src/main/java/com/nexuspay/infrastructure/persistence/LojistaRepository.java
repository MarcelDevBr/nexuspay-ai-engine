package com.nexuspay.infrastructure.persistence;

import com.nexuspay.domain.model.Lojista;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface LojistaRepository extends JpaRepository<Lojista, String> {
    Optional<Lojista> findByCnpjHash(String cnpjHash);
}
