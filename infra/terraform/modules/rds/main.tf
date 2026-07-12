terraform {
  required_version = ">= 1.7.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.60" }
  }
}

variable "name"                { type = string }
variable "vpc_id"              { type = string }
variable "private_subnet_ids"  { type = list(string) }
variable "instance_class"      { type = string  default = "db.t4g.medium" }
variable "allocated_storage"   { type = number  default = 100 }
variable "engine_version"      { type = string  default = "16.4" }
variable "multi_az"            { type = bool    default = true }
variable "backup_retention_days" { type = number default = 7 }
variable "kms_key_arn"         { type = string }
variable "tags"                { type = map(string) default = {} }

# --- Security group (only ECS tasks may connect) ---------------------------
resource "aws_security_group" "db" {
  name        = "${var.name}-db"
  description = "Postgres access from ECS tasks only"
  vpc_id      = var.vpc_id
  tags        = merge(var.tags, { Name = "${var.name}-db" })

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [] # <-- ECS task SGs attached by ecs-service module
    description     = "Postgres"
  }
}

# --- Subnet group -----------------------------------------------------------
resource "aws_db_subnet_group" "this" {
  name       = var.name
  subnet_ids = var.private_subnet_ids
  tags       = merge(var.tags, { Name = var.name })
}

# --- Parameter group --------------------------------------------------------
resource "aws_db_parameter_group" "pg16" {
  name   = "${var.name}-pg16"
  family = "postgres16"

  parameter { name = "rds.force_ssl"            value = "1"      apply_method = "immediate" }
  parameter { name = "log_statement"            value = "ddl"    apply_method = "immediate" }
  parameter { name = "shared_preload_libraries" value = "pg_stat_statements" apply_method = "pending-reboot" }
}

# --- Master credential (random, sourced from Secrets Manager in reality) ---
resource "random_password" "master" {
  length  = 32
  special = false
}

resource "aws_db_instance" "this" {
  identifier                          = var.name
  engine                              = "postgres"
  engine_version                      = var.engine_version
  instance_class                      = var.instance_class
  allocated_storage                   = var.allocated_storage
  storage_type                        = "gp3"
  storage_encrypted                   = true
  kms_key_id                          = var.kms_key_arn
  db_subnet_group_name                = aws_db_subnet_group.this.name
  vpc_security_group_ids              = [aws_security_group.db.id]
  parameter_group_name                = aws_db_parameter_group.pg16.name
  multi_az                            = var.multi_az
  backup_retention_period             = var.backup_retention_days
  backup_window                       = "05:00-05:30"
  maintenance_window                  = "sun:06:00-sun:07:00"
  deletion_protection                 = true
  copy_tags_to_snapshot               = true
  auto_minor_version_upgrade          = true
  iam_database_authentication_enabled = true
  performance_insights_enabled        = true
  performance_insights_retention_period = 7
  username                            = "postgres_admin"
  password                            = random_password.master.result
  publicly_accessible                 = false
  tags                                = merge(var.tags, { Name = var.name })

  lifecycle {
    ignore_changes = [password]
  }
}

# --- RDS Proxy (pooling — required for RLS SET LOCAL pattern D10) ----------
resource "aws_db_proxy" "this" {
  name                   = var.name
  engine_family          = "POSTGRESQL"
  role_arn               = aws_iam_role.proxy.arn
  vpc_subnet_ids         = var.private_subnet_ids
  vpc_security_group_ids = [aws_security_group.db.id]
  require_tls            = true
  tags                   = merge(var.tags, { Name = var.name })

  auth {
    auth_scheme = "SECRETS"
    iam_auth    = "REQUIRED"
    secret_arn  = aws_secretsmanager_secret.master.arn
  }
}

resource "aws_secretsmanager_secret" "master" {
  name       = "${var.name}/postgres/master"
  kms_key_id = var.kms_key_arn
  tags       = merge(var.tags, { Name = var.name })
}

resource "aws_secretsmanager_secret_version" "master" {
  secret_id = aws_secretsmanager_secret.master.id
  secret_string = jsonencode({
    username = aws_db_instance.this.username
    password = random_password.master.result
    engine   = "postgres"
    host     = aws_db_instance.this.address
    port     = 5432
    dbname   = "acquisition_os"
  })
}

resource "aws_iam_role" "proxy" {
  name = "${var.name}-rds-proxy"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{ Effect = "Allow", Principal = { Service = "rds.amazonaws.com" }, Action = "sts:AssumeRole" }]
  })
  tags = var.tags
}

output "endpoint"        { value = aws_db_instance.this.address }
output "port"            { value = aws_db_instance.this.port }
output "proxy_endpoint"  { value = aws_db_proxy.this.endpoint }
output "secret_arn"      { value = aws_secretsmanager_secret.master.arn }
output "security_group_id" { value = aws_security_group.db.id }
