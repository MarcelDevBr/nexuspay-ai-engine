# ==============================================================================
# Amazon EKS (Elastic Kubernetes Service) - NexusPay AI Engine
# ==============================================================================

resource "aws_iam_role" "eks_cluster_role" {
  name = "nexuspay-eks-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "eks.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks_cluster_role.name
}

resource "aws_eks_cluster" "nexuspay_eks" {
  name     = "nexuspay-eks-cluster"
  role_arn = aws_iam_role.eks_cluster_role.arn
  version  = "1.31"

  vpc_config {
    subnet_ids              = ["subnet-mock-1a", "subnet-mock-1b"]
    endpoint_public_access  = true
    endpoint_private_access = true
  }

  tags = {
    Environment = var.environment
    Project     = "NexusPay-AI-Engine"
    ManagedBy   = "Terraform"
    CostCenter  = "FinOps-ZeroBudget"
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_policy
  ]
}

# ==============================================================================
# Node Group FinOps (EC2 Spot Instances com Auto-Scaling e Travas de Custo)
# ==============================================================================

resource "aws_iam_role" "eks_node_role" {
  name = "nexuspay-eks-node-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "eks_worker_node_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.eks_node_role.name
}

resource "aws_iam_role_policy_attachment" "eks_cni_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.eks_node_role.name
}

resource "aws_iam_role_policy_attachment" "eks_container_registry" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.eks_node_role.name
}

resource "aws_eks_node_group" "nexuspay_spot_nodes" {
  cluster_name    = aws_eks_cluster.nexuspay_eks.name
  node_group_name = "nexuspay-spot-node-group"
  node_role_arn   = aws_iam_role.eks_node_role.arn
  subnet_ids      = ["subnet-mock-1a", "subnet-mock-1b"]

  capacity_type  = "SPOT"
  instance_types = ["t4g.medium", "t3.medium"]

  scaling_config {
    desired_size = 2
    max_size     = 4
    min_size     = 1
  }

  update_config {
    max_unavailable = 1
  }

  tags = {
    Environment = var.environment
    Lifecycle   = "Spot"
    ManagedBy   = "Terraform"
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_worker_node_policy,
    aws_iam_role_policy_attachment.eks_cni_policy,
    aws_iam_role_policy_attachment.eks_container_registry
  ]
}
