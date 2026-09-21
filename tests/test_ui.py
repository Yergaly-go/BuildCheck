from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_training_flow_renders_confirmed_evidence_result():
    app = AppTest.from_file(Path(__file__).parents[1] / "app.py")
    app.run()
    assert not app.exception
    assert app.button[0].label == "Анализировать"

    app.button[0].click().run()
    assert not app.exception
    assert any("CONFIRMED" in heading.value for heading in app.subheader)
    assert app.code[0].value == "NCR-014\nСтатус: ЗАКРЫТО"
    assert "страница: 1" in app.markdown[-1].value
