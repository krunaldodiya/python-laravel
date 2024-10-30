from typing import Any, Callable, Optional, Self, TypeVar, Generic
from Illuminate.Contracts.Collections.Collection import Collection as CollectionContract

T = TypeVar("T")


class Conditionable(Generic[T], CollectionContract):
    def when(
        self,
        value=None,
        callback: Optional[Callable[..., Any]] = None,
        default: Optional[Callable[..., Any]] = None,
    ) -> Self:
        value = value(self) if callable(value) else value

        if value:
            return callback(self, value) if callable(callback) else self
        else:
            return default(self, value) if callable(default) else self
