variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "Região AWS padrão"
}

variable "environment" {
  type        = string
  default     = "dev"
  description = "Ambiente de execução"
}

variable "is_localstack" {
  type        = bool
  default     = true
  description = "Define se o provisionamento aponta para LocalStack local (0 custo) ou AWS real"
}

variable "localstack_endpoint" {
  type        = string
  default     = "http://localhost:4566"
  description = "URL do endpoint LocalStack"
}

variable "alert_email" {
  type        = string
  default     = "alerta-finops@nexuspay.dev"
  description = "E-mail para recebimento de alertas de estouro de orçamento no AWS Budgets"
}
