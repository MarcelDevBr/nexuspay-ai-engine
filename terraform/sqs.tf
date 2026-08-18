# -----------------------------------------------------------------------------
# Filas SQS: Barramento de Eventos Transacionais do NexusPay
# -----------------------------------------------------------------------------

# Dead Letter Queue (DLQ) para mensagens que falharem após retentativas
resource "aws_sqs_queue" "transacoes_events_dlq" {
  name                      = "nexuspay-transacoes-events-dlq"
  message_retention_seconds = 1209600 # 14 dias
}

# Fila Principal de Eventos Transacionais
resource "aws_sqs_queue" "transacoes_events" {
  name                      = "transacoes-events"
  message_retention_seconds = 86400 # 1 dia
  visibility_timeout_seconds = 30

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.transacoes_events_dlq.arn
    maxReceiveCount     = 5
  })
}
