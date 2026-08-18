# ==============================================================================
# Amazon RDS PostgreSQL 16 com extensão nativa pgvector
# ==============================================================================

resource "aws_db_subnet_group" "nexuspay_db_subnet_group" {
  name       = "nexuspay-db-subnet-group"
  subnet_ids = ["subnet-mock-1a", "subnet-mock-1b"]

  tags = {
    Name        = "nexuspay-db-subnet-group"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_security_group" "rds_security_group" {
  name        = "nexuspay-rds-sg"
  description = "Security Group para o Amazon RDS PostgreSQL"
  vpc_id      = "vpc-mock-12345"

  ingress {
    description = "PostgreSQL do Cluster EKS"
    from_port   = 5432
    to_port     = 5432
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
    Name        = "nexuspay-rds-sg"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_db_parameter_group" "nexuspay_pg16_params" {
  name   = "nexuspay-pg16-parameters"
  family = "postgres16"

  parameter {
    name  = "shared_preload_libraries"
    value = "pg_stat_statements,pgvector"
  }

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_db_instance" "nexuspay_postgres" {
  identifier             = "nexuspay-postgres-instance"
  engine                 = "postgres"
  engine_version         = "16.4"
  instance_class         = "db.t4g.micro" # FinOps Free-Tier eligible
  allocated_storage      = 20
  max_allocated_storage  = 50
  storage_type           = "gp3"
  db_name                = "nexuspay_db"
  username               = "nexus_user"
  password               = "NexusSecureP@ssw0rd2026"
  db_subnet_group_name   = aws_db_subnet_group.nexuspay_db_subnet_group.name
  vpc_security_group_ids = [aws_security_group.rds_security_group.id]
  parameter_group_name   = aws_db_parameter_group.nexuspay_pg16_params.name
  skip_final_snapshot    = true
  publicly_accessible    = false

  tags = {
    Name        = "nexuspay-rds-postgres"
    Environment = var.environment
    Project     = "NexusPay-AI-Engine"
    FinOpsGuard = "FreeTierEligible"
    ManagedBy   = "Terraform"
  }
}
