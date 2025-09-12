import os
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_conversation():
    """Tests the /conversation endpoint."""
    # First, upload a document to have something to talk to
    test_pdf_path = "tests/test.pdf"
    if not os.path.exists(test_pdf_path):
        from .create_test_pdf import create_test_pdf
        create_test_pdf(test_pdf_path)

    with open(test_pdf_path, "rb") as f:
        upload_response = client.post("/api/upload", files={"file": ("test.pdf", f, "application/pdf")})

    assert upload_response.status_code == 200
    doc_id = upload_response.json()["docId"]

    # Now, test the conversation
    response = client.post(
        "/api/conversation",
        json={"docId": doc_id, "message": "What is this document about?"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert "Sources" in data
    assert "facts" in data["Sources"]
    assert "pages" in data["Sources"]
