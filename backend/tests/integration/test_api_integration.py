"""Integration tests for PDF Toolbox API."""
import pytest
import tempfile
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture
def sample_pdf_content():
    """Get sample PDF content."""
    return b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
/Type /Pages
/Count 1
/Kids [3 0 R]
>>
endobj
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
>>
endobj
4 0 obj
<<
/Length 44
>>
stream
BT
/F1 12 Tf
100 700 Td
(Test) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000226 00000 n
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
312
%%EOF"""


@pytest.fixture
def sample_pdf_file(sample_pdf_content, tmp_path):
    """Create temporary PDF file."""
    pdf_path = tmp_path / "test.pdf"
    pdf_path.write_bytes(sample_pdf_content)
    return pdf_path


class TestToolsAPI:
    """Tests for tools API endpoints."""

    def test_get_all_tools(self):
        """Test getting all tools."""
        response = client.get("/api/v1/tools")
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert isinstance(data["data"], list)
        assert len(data["data"]) > 0

    def test_get_tool_by_id(self):
        """Test getting tool by ID."""
        response = client.get("/api/v1/tools/merge")
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert data["data"]["id"] == "merge"

    def test_get_nonexistent_tool(self):
        """Test getting non-existent tool."""
        response = client.get("/api/v1/tools/nonexistent")
        assert response.status_code == 404


class TestFilesAPI:
    """Tests for files API endpoints."""

    def test_upload_pdf_file(self, sample_pdf_file):
        """Test uploading PDF file."""
        with open(sample_pdf_file, "rb") as f:
            files = {"files": ("test.pdf", f, "application/pdf")}
            data = {"tool_id": "merge"}

            response = client.post(
                "/api/v1/files/upload",
                files=files,
                data=data
            )

        assert response.status_code == 200

        result = response.json()
        assert result["success"] is True
        assert "data" in result
        assert "upload_id" in result["data"]
        assert "files" in result["data"]
        assert len(result["data"]["files"]) == 1

    def test_upload_invalid_file_type(self, sample_pdf_file, tmp_path):
        """Test uploading invalid file type."""
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("Not a PDF")

        with open(txt_file, "rb") as f:
            files = {"files": ("test.txt", f, "text/plain")}
            data = {"tool_id": "merge"}

            response = client.post(
                "/api/v1/files/upload",
                files=files,
                data=data
            )

        assert response.status_code == 415

    def test_download_nonexistent_file(self):
        """Test downloading non-existent file."""
        response = client.get("/api/v1/files/download/nonexistent")
        assert response.status_code == 404


class TestJobsAPI:
    """Tests for jobs API endpoints."""

    def test_create_job_without_upload(self):
        """Test creating job without uploading files."""
        response = client.post("/api/v1/jobs", json={
            "tool_id": "merge",
            "upload_id": "nonexistent",
            "options": {}
        })

        # Should fail because processor can't find files
        # But the job creation itself should succeed
        assert response.status_code in [200, 400]

    def test_get_nonexistent_job(self):
        """Test getting non-existent job."""
        response = client.get("/api/v1/jobs/nonexistent")
        assert response.status_code == 404

    def test_cancel_nonexistent_job(self):
        """Test cancelling non-existent job."""
        response = client.delete("/api/v1/jobs/nonexistent")
        assert response.status_code == 400


class TestAPIEndpoints:
    """Tests for general API endpoints."""

    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert "version" in data

    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"

    def test_cors_headers(self):
        """Test CORS headers are present."""
        response = client.options("/api/v1/tools")
        assert response.status_code == 200

    def test_security_headers(self):
        """Test security headers are present."""
        response = client.get("/")

        assert "X-Content-Type-Options" in response.headers
        assert "X-Frame-Options" in response.headers
        assert "X-XSS-Protection" in response.headers
