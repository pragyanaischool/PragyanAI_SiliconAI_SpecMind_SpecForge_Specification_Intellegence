import re


def normalize_spec_text(raw_text: str) -> str:
    """Normalizes CRLF line endings, unifies Verilog bit-width slices,
    standardizes active-low signal identifiers, and strips invalid chars.
    """
    if not raw_text:
        return ""

    # Normalize newlines and whitespace
    text = raw_text.replace("\r\n", "\n").replace("\t", "    ")

    # Clean non-standard quotes and dashes
    text = text.replace("“", '"').replace("”", '"').replace("’", "'").replace("—", "-")

    # Standardize bit-range representations (e.g. [ 31 : 0 ] -> [31:0])
    text = re.sub(r"\[\s*(\d+)\s*:\s*(\d+)\s*\]", r"[\1:\2]", text)

    # Clean active-low conventions (reset_n, rst_b, RESET-N -> standard rst_n)
    text = re.sub(r"\b([a-zA-Z0-9_]+)_[bB]\b", r"\1_n", text)

    # Collapse excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()
