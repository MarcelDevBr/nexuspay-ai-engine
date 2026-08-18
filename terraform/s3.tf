# ==============================================================================
# Amazon S3: Storage de Evidências, Recibos de Pagamento e Manuais RAG
# ==============================================================================

resource "aws_s3_bucket" "nexuspay_storage" {
  bucket        = "nexuspay-evidence-storage-${var.environment}"
  force_destroy = var.is_localstack

  tags = {
    Name        = "nexuspay-evidence-storage"
    Environment = var.environment
    Compliance  = "PCI-DSS-Vault"
    ManagedBy   = "Terraform"
  }
}

resource "aws_s3_bucket_versioning" "nexuspay_storage_versioning" {
  bucket = aws_s3_bucket.nexuspay_storage.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "nexuspay_storage_encryption" {
  bucket = aws_s3_bucket.nexuspay_storage.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "nexuspay_storage_lifecycle" {
  bucket = aws_s3_bucket.nexuspay_storage.id

  rule {
    id     = "archive-old-receipts-to-glacier-finops"
    status = "Enabled"

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    expiration {
      days = 1825 # 5 anos de retenção fiscal BACEN
    }
  }
}
