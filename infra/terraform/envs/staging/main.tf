terraform {
  required_version = ">= 1.7.0"

  backend "s3" {
    bucket         = "acquisition-os-tfstate-staging"
    key            = "staging/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "acquisition-os-tfstate-lock"
    encrypt        = true
  }

  required_providers {
    aws    = { source = "hashicorp/aws",    version = "~> 5.60" }
    random = { source = "hashicorp/random", version = "~> 3.6"  }
  }
}

provider "aws" {
  region = "us-east-1"
  default_tags {
    tags = {
      App         = "acquisition-os"
      Env         = "staging"
      ManagedBy   = "terraform"
      CostCenter  = "product"
    }
  }
}

# --- KMS master key ---------------------------------------------------------
resource "aws_kms_key" "master" {
  description             = "acquisition-os staging master CMK"
  deletion_window_in_days = 30
  enable_key_rotation     = true
}

resource "aws_kms_alias" "master" {
  name          = "alias/acquisition-os-staging"
  target_key_id = aws_kms_key.master.key_id
}

# --- Network ---------------------------------------------------------------
module "network" {
  source     = "../../modules/network"
  name       = "acquisition-os-staging"
  cidr_block = "10.20.0.0/16"
  az_count   = 3
}

# --- RDS Postgres 16 -------------------------------------------------------
module "rds" {
  source             = "../../modules/rds"
  name               = "acquisition-os-staging"
  vpc_id             = module.network.vpc_id
  private_subnet_ids = module.network.private_subnet_ids
  kms_key_arn        = aws_kms_key.master.arn
  engine_version     = "16.4"
  multi_az           = false # cost — flipped to true in prod
}

# --- ElastiCache (Valkey) --------------------------------------------------
module "cache" {
  source             = "../../modules/cache"
  name               = "acquisition-os-staging"
  vpc_id             = module.network.vpc_id
  private_subnet_ids = module.network.private_subnet_ids
}

# --- Secrets Manager -------------------------------------------------------
module "secrets" {
  source      = "../../modules/secrets"
  prefix      = "acquisition-os/staging"
  kms_key_arn = aws_kms_key.master.arn
  secrets = {
    "workos/api_key"        = "REPLACE_AT_APPLY"
    "workos/client_id"      = "REPLACE_AT_APPLY"
    "workos/jwks_url"       = "REPLACE_AT_APPLY"
    "stripe/api_key"        = "REPLACE_AT_APPLY"
    "gateway/litellm_master"= "REPLACE_AT_APPLY"
    "langfuse/public"       = "REPLACE_AT_APPLY"
    "langfuse/secret"       = "REPLACE_AT_APPLY"
    "meilisearch/host"      = "REPLACE_AT_APPLY"
    "meilisearch/api_key"   = "REPLACE_AT_APPLY"
  }
}

# --- Observability ---------------------------------------------------------
module "observability" {
  source = "../../modules/observability"
  name   = "acquisition-os-staging"
}

# --- ECS cluster -----------------------------------------------------------
resource "aws_ecs_cluster" "this" {
  name = "acquisition-os-staging"
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# The ecs-service module is invoked once per role (api, worker, temporal-worker).
# Wiring is intentionally minimal in Sprint 1 — the ALB + target group land in
# Sprint 2 with the deploy pipeline.

output "vpc_id"               { value = module.network.vpc_id }
output "rds_proxy_endpoint"   { value = module.rds.proxy_endpoint }
output "cache_endpoint"       { value = module.cache.primary_endpoint }
output "secret_arns"          { value = module.secrets.secret_arns }
output "cluster_arn"          { value = aws_ecs_cluster.this.arn }
