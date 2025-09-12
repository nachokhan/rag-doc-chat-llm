import fitz  # PyMuPDF

def parse_pdf(file_path: str) -> list[str]:
    """Extracts text from each page of a PDF file."""
    doc = fitz.open(file_path)
    pages = []
    for page in doc:
        pages.append(page.get_text())
    return pages
