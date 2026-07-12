terraform {
  required_version = ">= 1.7.0"
  required_providers { aws = { source = "hashicorp/aws", version = "~> 5.60" } }
}

# Grafana Cloud + Sentry credentials live in Secrets Manager; this module owns
# only the AWS-side plumbing (log groups + IAM to publish OTel to Grafana Cloud).

variable "name"        { type = string }
variable "tags"        { type = map(string) default = {} }

resource "aws_cloudwatch_log_group" "app" {
  name              = "/aos/${var.name}/app"
  retention_in_days = 30
  tags              = var.tags
}

# Placeholder for the OTel-Collector-to-Grafana-Cloud IAM role. Grafana Cloud's
# recommended pattern is a task IAM role assumed by the sidecar collector; we
# emit the ARN here so the ecs-service module can attach it.
resource "aws_iam_role" "otel_collector" {
  name = "${var.name}-otel-collector"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{ Effect = "Allow", Principal = { Service = "ecs-tasks.amazonaws.com" }, Action = "sts:AssumeRole" }]
  })
  tags = var.tags
}

output "log_group_name"       { value = aws_cloudwatch_log_group.app.name }
output "otel_collector_role"  { value = aws_iam_role.otel_collector.arn }
