import os
import tempfile
import pytest
from src.1_specification_intelligence.doc_understanding.text_normalizer import normalize_spec_text
from src.1_specification_intelligence.doc_understanding.pdf_table_parser import parse_pdf_with_tables
from src.rag.chunker import chunk_spec_document


def test_normalize_spec_text_basic():
    raw_sample = "Signal [  31 : 0 ]\r\ndata_in;\t\nreset_b is asserted low.\n\n\n\nNext section."
    normalized = normalize_spec_text(raw_sample)

    # Verifies bit range slice normalization [ 31 : 0 ] -> [31:0]
    assert "[31:0]" in normalized
    # Verifies CRLF replaced with newline
    assert "\r" not in normalized
    # Verifies active low naming conversion reset_b -> reset_n
    assert "reset_n" in normalized
    # Verifies excessive newlines collapsed
    assert "\n\n\n" not in normalized


def test_normalize_spec_text_quotes_and_dashes():
    raw_sample = '“Quad-SPI Mode”—asserts ‘CS_N’ signal.'
    normalized = normalize_spec_text(raw_sample)

    assert '"Quad-SPI Mode"' in normalized
    assert "'CS_N'" in normalized
    assert "-" in normalized


def test_chunk_spec_document_boundaries():
    text_sample = (
        "# Title\n\n"
        "## Interface Description\n"
        "[TABLE_START]\n"
        "| clk | input | [0:0] |\n"
        "| rst_n | input | [0:0] |\n"
        "[TABLE_END]\n\n"
        "## Timing Constraints\n"
        "Fmax is 250 MHz. Setup budget is 0.4ns."
    )
    chunks = chunk_spec_document(text_sample, chunk_size=300, chunk_overlap=50)

    assert len(chunks) >= 1
    # Verify table tokens are preserved
    combined_content = "".join([c.page_content for c in chunks])
    assert "[TABLE_START]" in combined_content
    assert "[TABLE_END]" in combined_content


def test_parse_pdf_with_tables_missing_file():
    with pytest.raises(FileNotFoundError):
        parse_pdf_with_tables("non_existent_datasheet.pdf")


def test_parse_pdf_with_tables_synthetic():
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
    from reportlab.lib.styles import getSampleStyleSheet

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        pdf_path = tmp.name

    try:
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = [
            Paragraph("Synthetic AXI Test Spec", styles["Heading1"]),
            Table([["Port", "Dir", "Width"], ["aclk", "in", "[0:0]"], ["tdata", "in", "[31:0]"]])
        ]
        doc.build(story)

        extracted = parse_pdf_with_tables(pdf_path)
        assert "PAGE 1" in extracted
        assert "aclk" in extracted
        assert "tdata" in extracted
    finally:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
