package com.nexuspay.infrastructure.persistence;

import com.nexuspay.domain.model.Transacao;
import com.nexuspay.domain.model.TransacaoId;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface TransacaoRepository extends JpaRepository<Transacao, TransacaoId> {
    List<Transacao> findByLojistaId(String lojistaId);
}
