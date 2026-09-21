from pathlib import Path

import pandas as pd
import streamlit as st

from buildcheck.evaluation import evaluate_requirement
from buildcheck.models import Requirement
from buildcheck.pdf_evidence import extract_ncr_evidence
from buildcheck.vision import VisionAdapter


TRAINING_DIR = Path(__file__).parent / "fixtures" / "training"


def load_training_requirement() -> Requirement:
    row = pd.read_csv(TRAINING_DIR / "checklist.csv").iloc[0]
    return Requirement(
        id=row["id"], text=row["text"], mandatory=bool(row["mandatory"]), evidence_type=row["evidence_type"]
    )


st.set_page_config(page_title="BuildCheck F001", layout="centered")
st.title("BuildCheck — F001 training slice")
st.caption("TRAINING only. Не является совместимым с реальными строительными документами.")

requirement = load_training_requirement()
st.subheader("Требование чек-листа")
st.write(requirement.text)

use_training = st.checkbox("Использовать TRAINING пример", value=True)
uploaded = st.file_uploader("Контрольный PDF", type=["pdf"])

if st.button("Анализировать", type="primary"):
    if uploaded is not None:
        pdf_bytes = uploaded.getvalue()
        source_name = uploaded.name
    elif use_training:
        pdf_bytes = (TRAINING_DIR / "control_closed.pdf").read_bytes()
        source_name = "TRAINING control_closed.pdf"
    else:
        pdf_bytes = b""
        source_name = "No document"

    evidence = extract_ncr_evidence(requirement, pdf_bytes, source_name) if pdf_bytes else []
    result = evaluate_requirement(requirement, evidence)
    st.subheader(f"Статус: {result.status}")
    st.write(result.deterministic_reason)
    st.write(f"Следующее действие: {result.next_action}")
    st.write("Ссылки на доказательства:", result.evidence_refs or "нет")
    for item in evidence:
        st.code(item.exact_excerpt, language=None)
        st.write(f"Источник: {item.source_document}; страница: {item.source_page}; качество: {item.evidence_quality}")

st.divider()
st.warning("Граница human review: результат не является автоматическим разрешением на бетонирование. Окончательное решение принимает инженер.")
st.caption(f"VISION_CAPABILITY = {VisionAdapter().describe_availability()}")
