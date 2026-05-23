"""
utils/pdf_utils.py — PDF text extraction using pdfplumber.
Also handles plain text files.
"""

import io
import streamlit as st


def extract_text_from_upload(uploaded_file) -> str:
    """
    Extract raw text from an uploaded PDF or TXT file.
    Returns cleaned string or raises ValueError.
    """
    if uploaded_file is None:
        raise ValueError("No file provided.")

    filename = uploaded_file.name.lower()
    file_bytes = uploaded_file.read()

    if filename.endswith(".pdf"):
        return _extract_from_pdf(file_bytes)
    elif filename.endswith(".txt"):
        return _extract_from_txt(file_bytes)
    else:
        raise ValueError(f"Unsupported file type: {filename}. Upload PDF or TXT.")


def _extract_from_pdf(file_bytes: bytes) -> str:
    """Extract text page-by-page using pdfplumber."""
    try:
        import pdfplumber
    except ImportError:
        raise ImportError("pdfplumber is required. Run: pip install pdfplumber")

    text_parts = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)

    if not text_parts:
        raise ValueError("Could not extract text. The PDF may be image-based or encrypted.")

    return "\n".join(text_parts).strip()


def _extract_from_txt(file_bytes: bytes) -> str:
    """Decode plain text, trying UTF-8 then latin-1."""
    for enc in ("utf-8", "latin-1", "cp1252"):
        try:
            text = file_bytes.decode(enc)
            if text.strip():
                return text.strip()
        except UnicodeDecodeError:
            continue
    raise ValueError("Could not decode the text file.")


def get_word_count(text: str) -> int:
    return len(text.split())


def get_char_count(text: str) -> int:
    return len(text)


def estimate_pages(text: str) -> int:
    """Rough estimate: ~500 words per page."""
    return max(1, round(get_word_count(text) / 500))
