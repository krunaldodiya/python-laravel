from abc import ABC, abstractmethod
from typing import Any, Dict


class Container(ABC):
    @abstractmethod
    def bind(self, key: str, binding_resolver: Any) -> None:
        """Bind a key to a resolver."""
        pass

    @abstractmethod
    def singleton(self, key: str, binding_resolver: Any) -> None:
        """Bind a key to a singleton resolver."""
        pass

    @abstractmethod
    def make(self, key: str, make_args: Dict[str, Any] = {}) -> Any:
        """Resolve and return an instance from the container."""
        pass

    @abstractmethod
    def bind_if(self, key: str, binding_resolver: Any) -> None:
        """Bind a key to a resolver if it is not already bound."""
        pass

    @abstractmethod
    def bound(self, key: str) -> Any:
        """Check if the key is already bound and return the instance if available."""
        pass

    @abstractmethod
    def instance(self, key: str, instance: Any) -> Any:
        """Store an instance in the container."""
        pass

    @abstractmethod
    def alias(self, abstract_alias: str, alias: Any) -> None:
        """Register an alias for an abstract."""
        pass

    @abstractmethod
    def get_alias(self, abstract: str) -> str:
        """Retrieve the alias for a given abstract."""
        pass

    @abstractmethod
    def get_bindings(self) -> Dict[str, Any]:
        """Return all bindings in the container."""
        pass

    @abstractmethod
    def get_instance(self, key: str) -> Any:
        """Retrieve a stored instance by key."""
        pass

    @abstractmethod
    def get_resolved(self) -> Dict[str, bool]:
        """Get all resolved bindings."""
        pass
