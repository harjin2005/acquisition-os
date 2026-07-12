terraform {
  required_version = ">= 1.7.0"
  required_providers { aws = { source = "hashicorp/aws", version = "~> 5.60" } }
}

variable "prefix"     { type = string }
variable "kms_key_arn"{ type = string }
variable "secrets"    { type = map(string) default = {} } # secret name -> initial value (rotated on first use)
variable "tags"       { type = map(string) default = {} }

resource "aws_secretsmanager_secret" "this" {
  for_each   = var.secrets
  name       = "${var.prefix}/${each.key}"
  kms_key_id = var.kms_key_arn
  tags       = merge(var.tags, { Name = "${var.prefix}/${each.key}" })
}

resource "aws_secretsmanager_secret_version" "this" {
  for_each      = var.secrets
  secret_id     = aws_secretsmanager_secret.this[each.key].id
  secret_string = each.value
  lifecycle { ignore_changes = [secret_string] } # rotated out-of-band
}

# --- IAM policy documents (attach to task role) -----------------------------
data "aws_iam_policy_document" "read" {
  statement {
    actions   = ["secretsmanager:GetSecretValue"]
    resources = [for s in aws_secretsmanager_secret.this : s.arn]
  }
  statement {
    actions   = ["kms:Decrypt"]
    resources = [var.kms_key_arn]
  }
}

resource "aws_iam_policy" "read" {
  name   = "${var.prefix}-secrets-read"
  policy = data.aws_iam_policy_document.read.json
  tags   = var.tags
}

output "secret_arns" {
  value = { for k, s in aws_secretsmanager_secret.this : k => s.arn }
}
output "read_policy_arn" { value = aws_iam_policy.read.arn }
