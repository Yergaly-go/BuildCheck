from enum import StrEnum

from pydantic import BaseModel, Field


class EvidenceQuality(StrEnum):
    RELIABLE = "RELIABLE"
    UNRELIABLE = "UNRELIABLE"


class ReadinessStatus(StrEnum):
    CONFIRMED = "CONFIRMED"
    ISSUE = "ISSUE"
    NEEDS_REVIEW = "NEEDS_REVIEW"


class Requirement(BaseModel):
    id: str
    text: str
    mandatory: bool
    evidence_type: str


class Evidence(BaseModel):
    requirement_id: str
    source_document: str
    source_page: int = Field(ge=1)
    exact_excerpt: str
    evidence_quality: EvidenceQuality
    image_region: tuple[float, float, float, float] | None = None


class Evaluation(BaseModel):
    requirement_id: str
    status: ReadinessStatus
    deterministic_reason: str
    evidence_refs: list[str]
    next_action: str
