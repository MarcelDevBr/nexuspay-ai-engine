terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.80"
    }
  }
}

provider "aws" {
  region                      = var.aws_region
  skip_credentials_validation = var.is_localstack
  skip_metadata_api_check     = var.is_localstack
  skip_requesting_account_id  = var.is_localstack

  dynamic "endpoints" {
    for_each = var.is_localstack ? [1] : []
    content {
      sqs            = var.localstack_endpoint
      s3             = var.localstack_endpoint
      secretsmanager = var.localstack_endpoint
    }
  }

  default_tags {
    tags = {
      Project     = "NexusPay-AI-Engine"
      Environment = var.environment
      ManagedBy   = "Terraform"
      FinOpsGuard = "FreeTierStrict"
    }
  }
}
