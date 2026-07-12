terraform {
  required_version = ">= 1.7.0"
  required_providers { aws = { source = "hashicorp/aws", version = "~> 5.60" } }
}

variable "name"             { type = string }
variable "vpc_id"           { type = string }
variable "private_subnet_ids"{ type = list(string) }
variable "node_type"        { type = string default = "cache.t4g.small" }
variable "num_shards"       { type = number default = 1 }
variable "replicas_per_shard" { type = number default = 1 }
variable "tags"             { type = map(string) default = {} }

resource "aws_elasticache_subnet_group" "this" {
  name       = var.name
  subnet_ids = var.private_subnet_ids
  tags       = merge(var.tags, { Name = var.name })
}

resource "aws_security_group" "cache" {
  name        = "${var.name}-cache"
  description = "Valkey access from ECS tasks only"
  vpc_id      = var.vpc_id
  tags        = merge(var.tags, { Name = "${var.name}-cache" })
}

resource "aws_elasticache_replication_group" "this" {
  replication_group_id       = var.name
  description                = "AcquisitionOS cache (Valkey engine — DOC-130 §5)"
  engine                     = "valkey"
  engine_version             = "7.2"
  node_type                  = var.node_type
  num_node_groups            = var.num_shards
  replicas_per_node_group    = var.replicas_per_shard
  automatic_failover_enabled = true
  multi_az_enabled           = true
  subnet_group_name          = aws_elasticache_subnet_group.this.name
  security_group_ids         = [aws_security_group.cache.id]
  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  tags                       = merge(var.tags, { Name = var.name })
}

output "primary_endpoint" { value = aws_elasticache_replication_group.this.primary_endpoint_address }
output "security_group_id" { value = aws_security_group.cache.id }
