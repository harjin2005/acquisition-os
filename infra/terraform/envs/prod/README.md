# Staging environment — DO NOT `apply` from the Emergent preview container.
#
# See `../staging/main.tf`. Sprint 1 leaves the prod environment as a stub;
# `envs/prod/main.tf` will land in Sprint 13 (Hardening & launch, DOC-131 E13)
# with the multi-AZ / cross-region backup posture and full ALB wiring.
#
# The stub is a deliberate "do not paste production configuration prematurely"
# guard — prod is a **destination**, not an early scaffolding target.
