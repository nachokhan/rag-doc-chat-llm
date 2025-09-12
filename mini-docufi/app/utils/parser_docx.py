import docx

def parse_docx(file_path: str) -> list[str]:
    """Extracts text from a DOCX file."""
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return ['\n'.join(full_text)]
