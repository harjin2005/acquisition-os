# Terraform — AcquisitionOS infrastructure

This directory is the canonical infrastructure-as-code for AcquisitionOS.

**Sprint 1 status:** modules are scaffolded but the staging environment is **not applied from this preview container** (Terraform cannot reach AWS from Emergent). Application to AWS runs from `.github/workflows/deploy.yml` on a merge to `main`, gated by manual approval for `prod` (DOC-130 §7).

## Layout

```
modules/
  network/          # VPC, subnets, NAT, egress security groups
  rds/              # Postgres 16 Multi-AZ + RDS Proxy
  cache/            # ElastiCache (Valkey engine)
  ecs-service/      # Fargate task + service + target group + autoscale
  secrets/          # Secrets Manager provisioning + IAM policy templates
  observability/    # Grafana Cloud + Sentry wiring
envs/
  staging/          # ap-southeast? us-east-1 tbd; staging account
  prod/             # prod account, RLS-mandatory
```

## Ground rules

- **State** in S3 + DynamoDB lock table (per env).
- **No console changes in prod.** Weekly drift check via `terraform plan -detailed-exitcode` in the `deploy.yml` workflow.
- **Modules are reusable.** Env root modules pin versions.
- **RLS is unforgeable.** The RDS module sets `rds.force_ssl=1` and creates the `acquisition_os` (app, RLS-enforced) and `acquisition_os_svc` (service, `BYPASSRLS`) roles at bootstrap via a one-shot Lambda migration; the app never has DDL rights in prod.
- **OIDC → AWS.** GitHub Actions authenticates via OIDC — no long-lived keys (DOC-130 §7).

## What still needs founder input before `apply`

1. AWS account IDs for `staging` and `prod`.
2. Region (default assumption: `us-east-1`; DOC-131 §7 defers to founder).
3. Domain(s) for ACM certificates.
4. WorkOS live credentials placed in Secrets Manager under `acquisition-os/{env}/workos/*`.
5. Design-partner IP allow-list decisions (if any) for staging ALB.

## Local dev

The preview environment does not require Terraform. `scripts/dev-up.sh` provisions Postgres directly.
