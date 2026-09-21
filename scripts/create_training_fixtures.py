"""Generate explicitly de-identified TRAINING PDFs for F001 tests and demo."""
from pathlib import Path

import pymupdf


TRAINING_DIR = Path(__file__).parents[1] / "fixtures" / "training"


def create_pdf(filename: str, status: str) -> None:
    document = pymupdf.open()
    page = document.new_page()
    page.insert_htmlbox(
        pymupdf.Rect(72, 72, 500, 200),
        f"<p>TRAINING CONTROL DOCUMENT<br>NCR-014<br>Статус: {status}</p>",
    )
    document.save(TRAINING_DIR / filename)
    document.close()


if __name__ == "__main__":
    TRAINING_DIR.mkdir(parents=True, exist_ok=True)
    create_pdf("control_closed.pdf", "ЗАКРЫТО")
    create_pdf("control_open.pdf", "ОТКРЫТО")
