terraform {
  required_version = ">= 1.7.0"
  required_providers { aws = { source = "hashicorp/aws", version = "~> 5.60" } }
}

variable "name"              { type = string }
variable "cluster_arn"       { type = string }
variable "vpc_id"            { type = string }
variable "private_subnet_ids"{ type = list(string) }
variable "image"             { type = string }
variable "container_port"    { type = number  default = 8001 }
variable "cpu"               { type = number  default = 512 }
variable "memory"            { type = number  default = 1024 }
variable "desired_count"     { type = number  default = 2 }
variable "env"               { type = map(string) default = {} }
variable "secrets"           { type = map(string) default = {} } # name -> secret ARN
variable "target_group_arn"  { type = string }
variable "task_role_arn"     { type = string }
variable "execution_role_arn"{ type = string }
variable "tags"              { type = map(string) default = {} }

resource "aws_security_group" "task" {
  name        = "${var.name}-task"
  description = "Egress-only for ${var.name}"
  vpc_id      = var.vpc_id
  tags        = merge(var.tags, { Name = "${var.name}-task" })

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "unrestricted egress; tighten per-service via NACL/VPC endpoints"
  }
}

resource "aws_cloudwatch_log_group" "task" {
  name              = "/ecs/${var.name}"
  retention_in_days = 30
  tags              = var.tags
}

locals {
  env_pairs      = [for k, v in var.env : { name = k, value = v }]
  secret_pairs   = [for k, arn in var.secrets : { name = k, valueFrom = arn }]
}

resource "aws_ecs_task_definition" "this" {
  family                   = var.name
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.cpu
  memory                   = var.memory
  execution_role_arn       = var.execution_role_arn
  task_role_arn            = var.task_role_arn

  container_definitions = jsonencode([
    {
      name         = var.name
      image        = var.image
      essential    = true
      portMappings = [{ containerPort = var.container_port, protocol = "tcp" }]
      environment  = local.env_pairs
      secrets      = local.secret_pairs
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.task.name
          awslogs-region        = data.aws_region.current.name
          awslogs-stream-prefix = "ecs"
        }
      }
      healthCheck = {
        command  = ["CMD-SHELL", "curl -f http://127.0.0.1:${var.container_port}/api/health || exit 1"]
        interval = 30
        timeout  = 5
        retries  = 3
      }
    }
  ])
  tags = var.tags
}

data "aws_region" "current" {}

resource "aws_ecs_service" "this" {
  name            = var.name
  cluster         = var.cluster_arn
  task_definition = aws_ecs_task_definition.this.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  deployment_configuration {
    minimum_healthy_percent = 50
    maximum_percent         = 200
    deployment_circuit_breaker {
      enable   = true
      rollback = true
    }
  }

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.task.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = var.target_group_arn
    container_name   = var.name
    container_port   = var.container_port
  }

  tags = merge(var.tags, { Name = var.name })
}

resource "aws_appautoscaling_target" "this" {
  service_namespace  = "ecs"
  resource_id        = "service/${var.cluster_arn}/${aws_ecs_service.this.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  min_capacity       = 2
  max_capacity       = 20
}

output "task_sg_id"        { value = aws_security_group.task.id }
output "service_name"      { value = aws_ecs_service.this.name }
output "task_definition_arn" { value = aws_ecs_task_definition.this.arn }
