"""PDF processors module."""
from app.processors.base import BaseProcessor
from app.processors.registry import ProcessorRegistry, registry

__all__ = ['BaseProcessor', 'ProcessorRegistry', 'registry']
