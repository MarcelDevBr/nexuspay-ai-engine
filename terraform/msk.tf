# ==============================================================================
# Amazon MSK (Managed Streaming for Apache Kafka) - NexusPay Event Streaming
# ==============================================================================

resource "aws_security_group" "msk_security_group" {
  name        = "nexuspay-msk-sg"
  description = "Security Group para o cluster Apache Kafka / Amazon MSK"
  vpc_id      = "vpc-mock-12345"

  ingress {
    description = "Kafka Plaintext / TLS"
    from_port   = 9092
    to_port     = 9098
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "nexuspay-msk-sg"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_msk_serverless_cluster" "nexuspay_kafka" {
  cluster_name = "nexuspay-kafka-cluster"

  vpc_config {
    subnet_ids         = ["subnet-mock-1a", "subnet-mock-1b"]
    security_group_ids = [aws_security_group.msk_security_group.id]
  }

  client_authentication {
    sasl {
      iam {
        enabled = true
      }
    }
  }

  tags = {
    Environment = var.environment
    Project     = "NexusPay-AI-Engine"
    ManagedBy   = "Terraform"
    FinOpsGuard = "ServerlessOnDemand"
  }
}
