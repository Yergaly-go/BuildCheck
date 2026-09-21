# Durable rules for BuildCheck

## Product and architecture boundaries

- BuildCheck is an evidence-first pre-pour readiness copilot, not an autonomous construction approver or field-record system of truth.
- Keep product decisions, domain policy, UI, integrations, and deployment concerns separate from core evaluation logic.
- Do not implement or imply capabilities that have not been explicitly specified and verified.

## Responsibilities and evidence

- Deterministic logic owns explicit, reproducible checks against structured and sufficient inputs.
- AI may interpret evidence, extract candidate observations, and explain uncertainty; it does not replace deterministic checks or qualified human judgment.
- Preserve evidence provenance: identify source, location/context, time when available, and the basis for every conclusion.
- Never invent measurements, field facts, evidence, provenance, or completion status.
- Not visible does not mean not present.
- Missing, ambiguous, contradictory, or insufficient evidence must resolve to `NEEDS_REVIEW`.
- Only use `CONFIRMED` when the available attributable evidence supports the check; use `ISSUE` only when evidence establishes a problem.
- No automatic construction approval: final approval is always a human decision.

## Engineering method and ownership

- Use R/F/R+F: reproduce or read the relevant context, fix only the scoped cause, then re-run the relevant verification plus focused regression checks.
- Each change must have a clear owner, purpose, and verification record; do not silently take ownership of unrelated existing work.
- Prefer small, reviewable changes with explicit interfaces and failure states.

## Failure and verification policy

- Fail safely: preserve the available evidence and report a clear `NEEDS_REVIEW` or explicit error; never manufacture a passing outcome.
- Verification claims must name what was actually checked. Untested, blocked, or uncertain work must be labeled accordingly.
- Treat unavailable tools, malformed input, and absent provenance as conditions to surface, not conditions to hide.

## Git safety

- Inspect status before editing and stage only named files.
- Inspect the staged diff before committing.
- Do not use broad staging, force pushes, destructive resets, or overwrite unrelated user changes.
- Keep commits scoped and describe only completed work.
