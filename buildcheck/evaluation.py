from buildcheck.models import Evidence, EvidenceQuality, Evaluation, ReadinessStatus, Requirement


ENGINEER_REVIEW_ACTION = (
    "No blocking action required for this requirement; engineer review remains required."
)


def evaluate_requirement(requirement: Requirement, evidence: list[Evidence]) -> Evaluation:
    """Deterministic F001 evaluator; it never infers a field condition from absence."""
    matching = [item for item in evidence if item.requirement_id == requirement.id]
    refs = [f"{item.source_document}:p{item.source_page}" for item in matching]
    if not matching:
        return Evaluation(
            requirement_id=requirement.id,
            status=ReadinessStatus.NEEDS_REVIEW,
            deterministic_reason="No attributable evidence was found; absence is not evidence of an issue.",
            evidence_refs=[],
            next_action="Provide reliable control-document evidence for engineer review.",
        )
    if any(item.evidence_quality != EvidenceQuality.RELIABLE for item in matching):
        return Evaluation(
            requirement_id=requirement.id,
            status=ReadinessStatus.NEEDS_REVIEW,
            deterministic_reason="Available evidence is ambiguous or unreliable.",
            evidence_refs=refs,
            next_action="Provide readable, attributable evidence for engineer review.",
        )
    if any("NCR-014" in item.exact_excerpt and "Статус: ОТКРЫТО" in item.exact_excerpt for item in matching):
        return Evaluation(
            requirement_id=requirement.id,
            status=ReadinessStatus.ISSUE,
            deterministic_reason="Reliable control-document evidence states that NCR-014 is ОТКРЫТО.",
            evidence_refs=refs,
            next_action="Close NCR-014 and provide updated control-document evidence for engineer review.",
        )
    if any("NCR-014" in item.exact_excerpt and "Статус: ЗАКРЫТО" in item.exact_excerpt for item in matching):
        return Evaluation(
            requirement_id=requirement.id,
            status=ReadinessStatus.CONFIRMED,
            deterministic_reason="Reliable control-document evidence states that NCR-014 is ЗАКРЫТО.",
            evidence_refs=refs,
            next_action=ENGINEER_REVIEW_ACTION,
        )
    return Evaluation(
        requirement_id=requirement.id,
        status=ReadinessStatus.NEEDS_REVIEW,
        deterministic_reason="The evidence does not deterministically establish the NCR-014 status.",
        evidence_refs=refs,
        next_action="Provide an explicit NCR-014 status for engineer review.",
    )
