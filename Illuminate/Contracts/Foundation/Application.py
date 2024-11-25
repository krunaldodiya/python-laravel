from abc import abstractmethod
from typing import Any, Type
from pathlib import Path

from Illuminate.Foundation.Console.Input.ArgvInput import ArgvInput
from Illuminate.Contracts.Container.Container import Container
from Illuminate.Http.RequestAdapter import RequestAdapter


class Application(Container):
    @property
    @abstractmethod
    def service_providers(self):
        """Returns the list of registered service providers."""
        pass

    @property
    @abstractmethod
    def loaded_providers(self):
        """Returns the loaded providers."""
        pass

    @abstractmethod
    def __getitem__(self, key: str) -> Any:
        """Gets the instance from the container."""
        pass

    @abstractmethod
    def is_booted(self) -> bool:
        """Checks if the application is booted."""
        pass

    @abstractmethod
    def has_been_bootstrapped(self) -> bool:
        """Checks if the application has been bootstrapped."""
        pass

    @abstractmethod
    def before_bootstraping(self, bootstrapper: str, callback: Any):
        """Registers a callback before bootstrapping."""
        pass

    @abstractmethod
    def after_bootstraping(self, bootstrapper: str, callback: Any):
        """Registers a callback after bootstrapping."""
        pass

    @abstractmethod
    def bootstrap_with(self, bootstrappers: list):
        """Bootstraps the application with the given bootstrappers."""
        pass

    @abstractmethod
    def base_path(self, path: str = "") -> Path:
        """Returns the base path of the application."""
        pass

    @abstractmethod
    def app_path(self, path: str = "") -> Path:
        """Returns the app path of the application."""
        pass

    @abstractmethod
    def use_app_path(self, path: Path):
        """Sets the application path."""
        pass

    @abstractmethod
    def config_path(self, path: str = "") -> Path:
        """Returns the config path of the application."""
        pass

    @abstractmethod
    def use_config_path(self, path: Path):
        """Sets the config path of the application."""
        pass

    @abstractmethod
    def bind(self, *args, **kwargs) -> None:
        """Binds an abstract to a concrete implementation."""
        pass

    @abstractmethod
    def singleton(self, *args, **kwargs) -> None:
        """Binds a singleton instance to the container."""
        pass

    @abstractmethod
    def make(self, *args, **kwargs) -> Any:
        """Resolves an instance from the container."""
        pass

    @abstractmethod
    def get_provider(self, base_key: str):
        """Gets the service provider by base key."""
        pass

    @abstractmethod
    def register_configured_providers(self) -> Any:
        """Registers providers configured in the application."""
        pass

    @abstractmethod
    def boot(self) -> Any:
        """Boots the application."""
        pass

    @abstractmethod
    def booting(self, callback: Any):
        """Registers a callback to be called during the booting process."""
        pass

    @abstractmethod
    def booted(self, callback: Any):
        """Registers a callback to be called after the boot process."""
        pass

    @abstractmethod
    def register(self, provider_class: Type):
        """Registers a service provider with the application."""
        pass

    @abstractmethod
    def boot_provider(self, service_provider: Any) -> Any:
        """Boots a service provider."""
        pass

    @abstractmethod
    def detect_environment(self, callback: Any):
        """Detects the application environment."""
        pass

    @abstractmethod
    def provider_is_loaded(self, base_key: str):
        """Gets the service provider by base key."""
        pass

    @abstractmethod
    def handle_request(self, request: RequestAdapter):
        """handle incoming request."""
        pass

    @abstractmethod
    def handle_command(self, input: ArgvInput):
        """handle command."""
        pass

    @abstractmethod
    def running_in_console(self) -> bool:
        """handle command."""
        pass

    @abstractmethod
    def set_running_in_console(self) -> "Application":
        """handle command."""
        pass
