# BuildCheck

BuildCheck is an **Evidence-First Pre-Pour Readiness Copilot**. It helps a human review the available pre-pour evidence, make the state of that evidence explicit, and identify items that need attention before a concrete pour.

## Intended workflow

1. Gather the available project evidence and its source context.
2. Evaluate deterministic checks where the required structured inputs exist.
3. Use AI only to interpret qualifying evidence and surface observations with provenance.
4. Classify each item as `CONFIRMED`, `ISSUE`, or `NEEDS_REVIEW`.
5. A designated human makes the final construction approval decision.

`CONFIRMED` means the available, attributable evidence supports the stated check. `ISSUE` means the available evidence establishes a problem. `NEEDS_REVIEW` means evidence is missing, ambiguous, insufficient, or requires qualified human judgment.

## Technology direction

The selected application direction is Python with Streamlit. The exact dependency set, storage design, integration boundaries, and deployment model remain `UNKNOWN` until they are deliberately decided.

## Main technical risk

The main risk is treating incomplete, ambiguous, or non-visible evidence as proof of field conditions. Product behavior must preserve provenance and uncertainty instead of converting inference into a construction-ready conclusion.

## Current scope

`NOT_IMPLEMENTED`: product features, UI, F001, vision-provider integration, data model, validation rules, tests, deployment, and approval workflow automation.

`UNKNOWN`: final functional requirements, user roles, evidence schema, source systems, model/provider choice, security requirements, retention policy, integrations, and acceptance criteria.
