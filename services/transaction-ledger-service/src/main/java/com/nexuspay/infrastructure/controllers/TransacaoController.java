package com.nexuspay.infrastructure.controllers;

import com.nexuspay.application.service.TransacaoService;
import com.nexuspay.infrastructure.controllers.dto.TransacaoRequest;
import com.nexuspay.infrastructure.controllers.dto.TransacaoResponse;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/transacoes")
public class TransacaoController {

    private final TransacaoService transacaoService;

    public TransacaoController(TransacaoService transacaoService) {
        this.transacaoService = transacaoService;
    }

    @PostMapping
    public ResponseEntity<TransacaoResponse> autorizarTransacao(@Valid @RequestBody TransacaoRequest request) {
        TransacaoResponse response = transacaoService.processarTransacao(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }
}
