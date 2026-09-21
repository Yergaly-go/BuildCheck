from io import BytesIO
import re

import pymupdf

from buildcheck.models import Evidence, EvidenceQuality, Requirement


STATUS_PATTERN = re.compile(r"(NCR-014\s*\n\s*Статус:\s*(?:ЗАКРЫТО|ОТКРЫТО))")


def extract_pages(pdf_bytes: bytes) -> list[str]:
    """Extract text per PDF page, preserving list index + 1 as its provenance page."""
    with pymupdf.open(stream=BytesIO(pdf_bytes), filetype="pdf") as document:
        return [page.get_text("text") for page in document]


def excerpt_exists_on_page(page_text: str, excerpt: str) -> bool:
    return bool(excerpt) and excerpt in page_text


def extract_ncr_evidence(
    requirement: Requirement, pdf_bytes: bytes, source_document: str
) -> list[Evidence]:
    """Return only grounded, exact status evidence found in the supplied PDF."""
    evidence: list[Evidence] = []
    for page_number, page_text in enumerate(extract_pages(pdf_bytes), start=1):
        for match in STATUS_PATTERN.finditer(page_text):
            excerpt = match.group(1)
            if excerpt_exists_on_page(page_text, excerpt):
                evidence.append(
                    Evidence(
                        requirement_id=requirement.id,
                        source_document=source_document,
                        source_page=page_number,
                        exact_excerpt=excerpt,
                        evidence_quality=EvidenceQuality.RELIABLE,
                    )
                )
    return evidence
