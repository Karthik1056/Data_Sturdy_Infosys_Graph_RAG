from app.services.cohort_service import build_competitive_cohort
from app.services.export_service import service_mapping, service_mapping_markdown


def test_default_cohort_shape():
    cohort = build_competitive_cohort("Infosys")
    assert cohort[0] == "Infosys"
    assert len(cohort) == 5


def test_custom_subject_insertion():
    cohort = build_competitive_cohort("Cognizant")
    assert cohort[0] == "Cognizant"
    assert len(cohort) == 5


def test_service_mapping_json():
    mapped = service_mapping(["Infosys", "TCS", "Accenture"])
    assert mapped["companies"] == ["Infosys", "TCS", "Accenture"]
    assert len(mapped["rows"]) == 2
    assert mapped["rows"][0]["Category"] == "AI Brand"
    assert mapped["rows"][1]["Category"] == "Cloud Brand"


def test_service_mapping_markdown_contains_headers():
    md = service_mapping_markdown(["Infosys", "TCS", "Accenture"])
    assert "| Category | Infosys | TCS | Accenture |" in md
    assert "| AI Brand |" in md
    assert "| Cloud Brand |" in md
