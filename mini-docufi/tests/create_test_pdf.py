from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_test_pdf(file_path: str):
    """Creates a simple PDF for testing."""
    c = canvas.Canvas(file_path, pagesize=letter)
    c.drawString(100, 750, "This is a test PDF document.")
    c.drawString(100, 735, "It contains some text for parsing.")
    c.save()

if __name__ == "__main__":
    create_test_pdf("tests/test.pdf")
