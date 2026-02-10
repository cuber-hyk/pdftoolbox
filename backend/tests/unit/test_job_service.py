"""Unit tests for job service."""
import pytest
from datetime import datetime
from app.services.job_service import JobService


def test_create_job():
    """Test job creation."""
    service = JobService()

    job = service.create_job(
        tool_id="merge",
        upload_id="ul_test123",
        options={"output_filename": "merged.pdf"}
    )

    assert job['job_id'].startswith("job_")
    assert job['tool_id'] == "merge"
    assert job['upload_id'] == "ul_test123"
    assert job['status'] == "queued"
    assert job['progress'] == 0
    assert job['options'] == {"output_filename": "merged.pdf"}


def test_get_job():
    """Test retrieving job."""
    service = JobService()

    job = service.create_job("merge", "ul_test", {})
    job_id = job['job_id']

    retrieved = service.get_job(job_id)
    assert retrieved is not None
    assert retrieved['job_id'] == job_id


def test_get_nonexistent_job():
    """Test retrieving non-existent job."""
    service = JobService()

    job = service.get_job("nonexistent")
    assert job is None


def test_update_job():
    """Test updating job."""
    service = JobService()

    job = service.create_job("merge", "ul_test", {})
    job_id = job['job_id']

    service.update_job(job_id, progress=50, message="Processing...")

    updated = service.get_job(job_id)
    assert updated['progress'] == 50
    assert updated['message'] == "Processing..."


def test_complete_job():
    """Test marking job as completed."""
    service = JobService()

    job = service.create_job("merge", "ul_test", {})
    job_id = job['job_id']

    result = {
        "output_file_id": "f_result",
        "filename": "output.pdf",
        "size": 1024
    }

    service.complete_job(job_id, result)

    completed = service.get_job(job_id)
    assert completed['status'] == "completed"
    assert completed['progress'] == 100
    assert completed['result'] == result


def test_fail_job():
    """Test marking job as failed."""
    service = JobService()

    job = service.create_job("merge", "ul_test", {})
    job_id = job['job_id']

    error = {"code": "ERR_TEST", "message": "Test error"}

    service.fail_job(job_id, error)

    failed = service.get_job(job_id)
    assert failed['status'] == "failed"
    assert failed['error'] == error


def test_cancel_job():
    """Test cancelling job."""
    service = JobService()

    job = service.create_job("merge", "ul_test", {})
    job_id = job['job_id']

    # Cancel queued job
    success = service.cancel_job(job_id)
    assert success is True

    cancelled = service.get_job(job_id)
    assert cancelled['status'] == "cancelled"


def test_cancel_completed_job():
    """Test cancelling completed job fails."""
    service = JobService()

    job = service.create_job("merge", "ul_test", {})
    job_id = job['job_id']

    # Complete job first
    service.complete_job(job_id, {})

    # Try to cancel
    success = service.cancel_job(job_id)
    assert success is False
