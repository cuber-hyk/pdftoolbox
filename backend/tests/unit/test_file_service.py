"""Unit tests for file service."""
import pytest
from pathlib import Path
from app.services.file_service import FileService


def test_generate_file_id():
    """Test file ID generation."""
    service = FileService()
    file_id = service.generate_file_id()

    assert file_id.startswith("f_")
    assert len(file_id) > 10


def test_generate_upload_id():
    """Test upload ID generation."""
    service = FileService()
    upload_id = service.generate_upload_id()

    assert upload_id.startswith("ul_")
    assert len(upload_id) > 10


def test_get_file_path():
    """Test file path generation."""
    service = FileService()
    file_id = "f_test123"
    file_path = service.get_file_path(file_id)

    assert file_id in file_path
    assert file_path.endswith(".pdf")


@pytest.mark.asyncio
async def test_save_and_delete_file(temp_pdf_file, tmp_path):
    """Test file save and delete operations."""
    from app.core.config import settings
    import os

    # Override settings for testing
    original_upload_dir = settings.UPLOAD_DIR
    settings.UPLOAD_DIR = str(tmp_path)

    try:
        service = FileService()
        file_id = service.generate_file_id()

        # Create a mock upload file
        class MockUploadFile:
            def __init__(self, path, filename):
                self.path = path
                self.filename = filename
                self.content_type = "application/pdf"

            async def read(self):
                return self.path.read_bytes()

            def seek(self, pos):
                self.path = Path(self.path)

        mock_file = MockUploadFile(temp_pdf_file, "test.pdf")

        # Save file
        result = await service.save_uploaded_file(mock_file, file_id)

        assert result['file_id'] == file_id
        assert result['name'] == "test.pdf"
        assert result['size'] > 0
        assert result['pages'] >= 0

        # Check file exists
        file_path = service.get_file_path(file_id)
        assert Path(file_path).exists()

        # Delete file
        deleted = service.delete_file(file_id)
        assert deleted is True
        assert not Path(file_path).exists()

    finally:
        settings.UPLOAD_DIR = original_upload_dir
