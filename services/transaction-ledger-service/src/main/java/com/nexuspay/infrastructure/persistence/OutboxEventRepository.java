package com.nexuspay.infrastructure.persistence;

import com.nexuspay.domain.model.OutboxEvent;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface OutboxEventRepository extends JpaRepository<OutboxEvent, UUID> {

    @Query("SELECT e FROM OutboxEvent e WHERE e.status = 'PENDENTE' ORDER BY e.criadoEm ASC")
    List<OutboxEvent> findTopPendingEvents(Pageable pageable);
}
