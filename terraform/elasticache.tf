# ==============================================================================
# Amazon ElastiCache for Redis 7 (Cache Semântico & Rate Limiting)
# ==============================================================================

resource "aws_elasticache_subnet_group" "nexuspay_redis_subnet_group" {
  name       = "nexuspay-redis-subnet-group"
  subnet_ids = ["subnet-mock-1a", "subnet-mock-1b"]

  tags = {
    Name        = "nexuspay-redis-subnet-group"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_security_group" "redis_security_group" {
  name        = "nexuspay-redis-sg"
  description = "Security Group para o Amazon ElastiCache Redis"
  vpc_id      = "vpc-mock-12345"

  ingress {
    description = "Redis do Cluster EKS"
    from_port   = 6379
    to_port     = 6379
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
    Name        = "nexuspay-redis-sg"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_elasticache_cluster" "nexuspay_redis" {
  cluster_id           = "nexuspay-redis-cluster"
  engine               = "redis"
  node_type            = "cache.t4g.micro" # FinOps Free Tier
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  port                 = 6379
  subnet_group_name    = aws_elasticache_subnet_group.nexuspay_redis_subnet_group.name
  security_group_ids   = [aws_security_group.redis_security_group.id]

  tags = {
    Name        = "nexuspay-redis-cache"
    Environment = var.environment
    Project     = "NexusPay-AI-Engine"
    FinOpsGuard = "FreeTierEligible"
    ManagedBy   = "Terraform"
  }
}
