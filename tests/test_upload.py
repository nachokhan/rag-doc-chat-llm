import os
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_upload_file():
    """Tests the /upload endpoint with a mock PDF file."""
    # Ensure the test file exists
    test_pdf_path = "tests/test.pdf"
    if not os.path.exists(test_pdf_path):
        from .create_test_pdf import create_test_pdf
        create_test_pdf(test_pdf_path)

    with open(test_pdf_path, "rb") as f:
        response = client.post("/api/upload", files={"file": ("test.pdf", f, "application/pdf")})

    assert response.status_code == 200
    assert "docId" in response.json()
