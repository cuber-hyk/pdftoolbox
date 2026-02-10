"""Processor registry for tool registration."""
from typing import Dict, Type, Optional
from app.processors.base import BaseProcessor


class ProcessorRegistry:
    """Registry for PDF processors."""

    def __init__(self) -> None:
        """Initialize registry."""
        self._processors: Dict[str, Type[BaseProcessor]] = {}

    def register(self, tool_id: str):
        """Decorator to register processor.

        Args:
            tool_id: Tool identifier

        Returns:
            Decorator function
        """
        def decorator(processor_class: Type[BaseProcessor]) -> Type[BaseProcessor]:
            """Register processor class.

            Args:
                processor_class: Processor class to register

            Returns:
                The same processor class
            """
            self._processors[tool_id] = processor_class
            return processor_class
        return decorator

    def get(self, tool_id: str) -> Optional[Type[BaseProcessor]]:
        """Get processor by tool ID.

        Args:
            tool_id: Tool identifier

        Returns:
            Processor class or None if not found
        """
        return self._processors.get(tool_id)

    def get_all(self) -> Dict[str, Type[BaseProcessor]]:
        """Get all registered processors.

        Returns:
            Dictionary of tool_id -> processor class
        """
        return self._processors.copy()

    def exists(self, tool_id: str) -> bool:
        """Check if processor exists.

        Args:
            tool_id: Tool identifier

        Returns:
            True if processor exists
        """
        return tool_id in self._processors


# Global registry instance
registry = ProcessorRegistry()
