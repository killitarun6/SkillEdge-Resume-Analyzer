from typing import IO
import io
import fitz  # PyMuPDF
from pdfminer.high_level import extract_text as pdfminer_text
from docx import Document

def _pdf_text_pymupdf(file_bytes: bytes) -> str:
    text_parts = []
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text_parts.append(page.get_text())
    return "\n".join(text_parts).strip()

def _pdf_text_pdfminer(file_bytes: bytes) -> str:
    fp = io.BytesIO(file_bytes)
    return pdfminer_text(fp)

def _docx_text(file_bytes: bytes) -> str:
    fp = io.BytesIO(file_bytes)
    doc = Document(fp)
    return "\n".join([p.text for p in doc.paragraphs]).strip()

def extract_text(uploaded_file: IO[bytes]) -> str:
    """
    Extract text from a Streamlit UploadedFile (PDF or DOCX).
    """
    name = uploaded_file.name.lower()
    data = uploaded_file.read()

    if name.endswith(".pdf"):
        try:
            return _pdf_text_pymupdf(data)
        except Exception:
            return _pdf_text_pdfminer(data)
    elif name.endswith(".docx"):
        return _docx_text(data)
    else:
        raise ValueError("Unsupported file type. Please upload a PDF or DOCX.")
