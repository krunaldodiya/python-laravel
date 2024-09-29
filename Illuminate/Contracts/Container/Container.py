from abc import ABC, abstractmethod
from typing import Any, Dict, Callable, Optional


class Container(ABC):
    @abstractmethod
    def bind(self, key: str, binding_resolver: Callable) -> None:
        """Bind a key to a binding resolver."""
        pass

    @abstractmethod
    def singleton(self, key: str, binding_resolver: Callable) -> None:
        """Bind a key to a binding resolver as a singleton."""
        pass

    @abstractmethod
    def make(self, key: str, make_args: Optional[Dict[str, Any]] = None) -> Any:
        """Resolve and create an instance of the given key."""
        pass

    @abstractmethod
    def bound(self, key: str) -> bool:
        """Check if a key is bound in the container."""
        pass

    @abstractmethod
    def alias(self, abstract_alias: str, alias: str) -> None:
        """Create an alias for an abstract key."""
        pass

    @abstractmethod
    def instance(self, key: str, instance: Any) -> Any:
        """Register an instance with a specific key."""
        pass

    @abstractmethod
    def forget_binding(self, key: str) -> None:
        """Remove a binding from the container."""
        pass

    @abstractmethod
    def forget_instance(self, key: str) -> None:
        """Remove an instance from the container."""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reset the container, clearing all bindings and instances."""
        pass

    @abstractmethod
    def has(self, key: str) -> bool:
        """Check if a key exists in the container."""
        pass

    @abstractmethod
    def get_aliases(self) -> Dict[str, str]:
        """Retrieve all aliases in the container."""
        pass

    @abstractmethod
    def get_bindings(self) -> Dict[str, Dict[str, Any]]:
        """Retrieve all bindings in the container."""
        pass

    @abstractmethod
    def get_instances(self) -> Dict[str, Any]:
        """Retrieve all instances in the container."""
        pass

    @abstractmethod
    def get_resolved(self) -> Dict[str, bool]:
        """Retrieve the resolved status of bindings."""
        pass
