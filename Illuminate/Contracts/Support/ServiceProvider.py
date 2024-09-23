from abc import ABC, abstractmethod


class ServiceProvider(ABC):
    @property
    @abstractmethod
    def booting_callbacks(self):
        """Returns the registered booting callbacks."""
        pass

    @property
    @abstractmethod
    def booted_callbacks(self):
        """Returns the registered booted callbacks."""
        pass

    @abstractmethod
    def register(self):
        """Registers services in the container."""
        pass

    @abstractmethod
    def boot(self):
        """Boots the services."""
        pass

    @abstractmethod
    def booting(self, callback):
        """Registers a booting callback."""
        pass

    @abstractmethod
    def booted(self, callback):
        """Registers a booted callback."""
        pass

    @abstractmethod
    def call_booting_callbacks(self):
        """Calls the registered booting callbacks."""
        pass

    @abstractmethod
    def call_booted_callbacks(self):
        """Calls the registered booted callbacks."""
        pass
