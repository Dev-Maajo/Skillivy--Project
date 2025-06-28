import os
import docx2txt
import fitz  # PyMuPDF
from PyPDF2 import PdfReader  # fallback if fitz fails

def extract_text_from_pdf(pdf_path):
    try:
        # Preferred way with fitz (PyMuPDF)
        text = ""
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
        if text.strip():
            return text.strip()

        # Fallback if PyMuPDF fails to extract
        raise ValueError("fitz returned empty text, trying fallback...")
    except Exception as e:
        try:
            # Fallback: use PyPDF2
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text.strip() if text.strip() else f"❌ PDF could not be parsed properly: {str(e)}"
        except Exception as fallback_error:
            return f"❌ Error reading PDF: {str(e)} | Fallback error: {str(fallback_error)}"

def extract_text_from_docx(docx_path):
    try:
        return docx2txt.process(docx_path).strip()
    except Exception as e:
        return f"❌ Error reading DOCX: {str(e)}"

def parse_resume(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        return "❌ Unsupported file format. Please upload a .pdf or .docx file."
