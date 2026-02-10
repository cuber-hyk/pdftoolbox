"""Unit tests for processor registry."""
import pytest
from app.processors.registry import ProcessorRegistry
from app.processors.base import BaseProcessor


class MockProcessor(BaseProcessor):
    """Mock processor for testing."""

    async def process(self, job_id: str, files, options):
        return f"result_{job_id}"


def test_registry_registration():
    """Test processor registration."""
    registry = ProcessorRegistry()

    # Register processor
    @registry.register("test_tool")
    class TestProcessor(BaseProcessor):
        async def process(self, job_id: str, files, options):
            return "test_result"

    # Check processor exists
    assert registry.exists("test_tool")
    assert registry.get("test_tool") is TestProcessor


def test_registry_get_nonexistent():
    """Test getting non-existent processor."""
    registry = ProcessorRegistry()

    assert registry.get("nonexistent") is None
    assert not registry.exists("nonexistent")


def test_registry_get_all():
    """Test getting all processors."""
    registry = ProcessorRegistry()

    @registry.register("tool1")
    class Tool1Processor(BaseProcessor):
        async def process(self, job_id: str, files, options):
            return "tool1"

    @registry.register("tool2")
    class Tool2Processor(BaseProcessor):
        async def process(self, job_id: str, files, options):
            return "tool2"

    all_processors = registry.get_all()
    assert "tool1" in all_processors
    assert "tool2" in all_processors
    assert len(all_processors) == 2
