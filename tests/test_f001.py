from pathlib import Path

from buildcheck.evaluation import evaluate_requirement
from buildcheck.models import Evidence, EvidenceQuality, ReadinessStatus, Requirement
from buildcheck.pdf_evidence import excerpt_exists_on_page, extract_ncr_evidence, extract_pages
from buildcheck.vision import VisionAdapter, VisionCapability


ROOT = Path(__file__).parents[1]
TRAINING = ROOT / "fixtures" / "training"
REQUIREMENT = Requirement(
    id="REQ-NCR-014",
    text="Все блокирующие замечания должны быть закрыты до проверки готовности к бетонированию.",
    mandatory=True,
    evidence_type="control_document",
)


def evidence_from(name: str):
    return extract_ncr_evidence(REQUIREMENT, (TRAINING / name).read_bytes(), f"TRAINING {name}")


def test_pdf_page_provenance_and_exact_excerpt_are_preserved():
    pages = extract_pages((TRAINING / "control_closed.pdf").read_bytes())
    evidence = evidence_from("control_closed.pdf")
    assert len(pages) == 1
    assert evidence[0].source_page == 1
    assert excerpt_exists_on_page(pages[0], evidence[0].exact_excerpt)
    assert evidence[0].exact_excerpt == "NCR-014\nСтатус: ЗАКРЫТО"


def test_closed_is_confirmed():
    result = evaluate_requirement(REQUIREMENT, evidence_from("control_closed.pdf"))
    assert result.status == ReadinessStatus.CONFIRMED
    assert result.next_action == "No blocking action required for this requirement; engineer review remains required."


def test_open_is_issue():
    result = evaluate_requirement(REQUIREMENT, evidence_from("control_open.pdf"))
    assert result.status == ReadinessStatus.ISSUE


def test_ambiguous_evidence_needs_review():
    ambiguous = Evidence(
        requirement_id=REQUIREMENT.id,
        source_document="TRAINING unreadable.pdf",
        source_page=1,
        exact_excerpt="NCR-014\nСтатус: НЕРАЗБОРЧИВО",
        evidence_quality=EvidenceQuality.UNRELIABLE,
    )
    assert evaluate_requirement(REQUIREMENT, [ambiguous]).status == ReadinessStatus.NEEDS_REVIEW


def test_missing_evidence_is_not_automatically_issue():
    assert evaluate_requirement(REQUIREMENT, []).status == ReadinessStatus.NEEDS_REVIEW


def test_vision_provider_cannot_set_final_status():
    adapter = VisionAdapter()
    assert adapter.describe_availability() == VisionCapability.UNAVAILABLE
    assert not hasattr(adapter, "set_final_status")
