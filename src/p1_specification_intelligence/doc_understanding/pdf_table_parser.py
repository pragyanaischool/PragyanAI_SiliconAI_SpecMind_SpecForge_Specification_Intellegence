import os
from typing import List
from pypdf import PdfReader


def parse_pdf_with_tables(pdf_path: str) -> str:
    """Extracts text and tabular content from PDF datasheets.

    Prioritizes pdfplumber for table preservation and falls back to pypdf.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF spec not found at: {pdf_path}")

    extracted_sections: List[str] = []

    try:
        import pdfplumber  # type: ignore

        with pdfplumber.open(pdf_path) as pdf:
            for page_idx, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text() or ""
                tables = page.extract_tables()

                extracted_sections.append(f"--- PAGE {page_idx} ---")
                if page_text:
                    extracted_sections.append(page_text)

                for table in tables:
                    if not table:
                        continue
                    extracted_sections.append("\n[TABLE_START]")
                    for row in table:
                        clean_row = [
                            str(col).strip().replace("\n", " ") if col else ""
                            for col in row
                        ]
                        extracted_sections.append("| " + " | ".join(clean_row) + " |")
                    extracted_sections.append("[TABLE_END]\n")
        return "\n".join(extracted_sections)

    except ImportError:
        reader = PdfReader(pdf_path)
        for page_idx, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            extracted_sections.append(f"--- PAGE {page_idx} ---\n{text}")

        return "\n".join(extracted_sections)
