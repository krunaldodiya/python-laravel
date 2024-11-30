import math

from typing import Any, Callable, Dict, Generic, List, Optional, Self, Tuple, Union
from typing_extensions import TypeVar
from Illuminate.Collections.Arr import Arr
from Illuminate.Collections.Traits.EnumeratesValues import EnumeratesValues
from Illuminate.Helpers.Util import Util
from Illuminate.Contracts.Collections.Collection import Collection as CollectionContract

T = TypeVar("T")


class Collection(EnumeratesValues, Generic[T], CollectionContract):
    def __init__(self, items={}, *args, **kwargs) -> None:
        self._items = self._get_iterable_items(items)

    def all(self):
        return [(key, item) for key, item in self._items.items()]

    def count(self) -> int:
        return len(self._items)

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def is_not_empty(self) -> bool:
        return not self.is_empty()

    def to_base(self) -> "Collection":
        return Collection(self._items)

    def values(self) -> Self:
        return self.__class__(self.to_list())

    def tap(self, callback: Callable[..., Any]) -> Self:
        callback(self)

        return self

    def prepend(self, value, key=None) -> Self:
        key = key if key else self._get_key()

        self._items = {key: value, **self._items}

        return self

    def filter(self, callback: Optional[Callable[..., Any]] = None) -> Self:
        if not callback:
            return self.__class__({key: value for key, value in self if value})

        self._check_is_callable(callback)

        results = {
            key: value
            for key, value in self
            if Util.callback_with_dynamic_args(callback, [value, key])
        }

        return self.__class__(results)

    def flat_map(self, callback: Callable[..., Any]) -> Self:
        return self.map(callback).flatten()

    def map(self, callback: Callable[..., Any]) -> Self:
        self._check_is_callable(callback)

        results = {
            key: Util.callback_with_dynamic_args(callback, [value, key])
            for key, value in self
        }

        return self.__class__(results)

    def map_with_keys(self, callback: Callable[..., Any]) -> Self:
        self._check_is_callable(callback)

        results = {}

        for key, value in self._items.items():
            assoc: dict = Util.callback_with_dynamic_args(callback, [value, key])

            for map_key, map_value in assoc.items():
                results[map_key] = map_value

        return self.__class__(results)

    def first(
        self, callback: Optional[Callable[[Any], bool]] = None, default=None
    ) -> Any:
        items = self._items

        if callback:
            items = self.filter(callback)._items

        return list(items.values())[0] if items else default

    def last(
        self, callback: Optional[Callable[[Any], bool]] = None, default=None
    ) -> Any:
        items = self._items

        if callback:
            items = self.filter(callback)._items

        return list(items.values())[-1] if items else default

    def push(self, value) -> Self:
        key = self._get_key()

        self._items[key] = value

        return self

    def pull(self, key, default=None) -> Self:
        return Arr.pull(self._items, key, default)

    def get(self, key, default=None) -> Self:
        return self._items[key] if key in self._items else default

    def unique(self, key: Optional[Callable] = None) -> Self:
        if not key:
            unique_values = set(self._items.values())

            return self.__class__(
                {key: value for key, value in enumerate(unique_values)}
            )

        callback = self._value_retriever(key)

        exists = []

        def is_unique(value, key):
            id = Util.callback_with_dynamic_args(callback, [value, key])

            if id in exists:
                return True

            exists.append(id)

        return self.reject(is_unique)

    def transform(self, callback: Callable[..., Any]) -> Self:
        self._items = self.map(callback)._items

        return self

    def concat(self, data: Union[List[Any], Dict[Any, Any], "Collection"] = []) -> Self:
        if isinstance(data, list):
            iterator = enumerate(data)
        elif isinstance(data, dict):
            iterator = data.items()
        elif isinstance(data, Collection):
            iterator = data.all()
        else:
            raise Exception(
                "Invalid items iterator, must be list, dict, or Collection object."
            )

        results = self.__class__(self._items)

        if not data:
            return results

        for key, item in iterator:
            results.push(item)

        return results

    def flatten(self, depth=math.inf) -> Self:
        flattened_items = Arr.flatten(self, depth)

        return self.__class__(flattened_items)

    def group_by(self, callback_or_string: Union[Callable[..., Any], str]):
        group_callback = self._value_retriever(callback_or_string)

        results: Dict[Any, Collection] = {}

        for key, value in self:
            group_keys = Util.callback_with_dynamic_args(group_callback, [value, key])

            def get_group_keys(group_keys):
                if isinstance(group_keys, str):
                    return [group_keys]

            group_keys = get_group_keys(group_keys) or [""]

            for group_key in group_keys:
                results.setdefault(group_key, self.__class__({})).push(value)

        return self.__class__(results)

    def sort_by(
        self,
        callback_or_string: Union[Callable[..., Any], str],
        descending: bool = False,
    ) -> Self:
        sort_callback = self._value_retriever(callback_or_string)

        sorted_items = self._sort_items(
            self.all(),
            key=lambda item: Util.callback_with_dynamic_args(
                sort_callback, [item[1], item[0]]
            ),
            descending=descending,
        )

        return self.__class__(sorted_items)

    def sort(
        self,
        sort_callback: Optional[Callable[..., Any]] = None,
        descending: bool = False,
    ) -> Self:
        if sort_callback:
            self._check_is_callable(sort_callback)

            return self.sort_by(sort_callback, descending)

        sorted_items = self._sort_items(
            self.all(), key=lambda item: str(item[1]), descending=descending
        )

        return self.__class__(sorted_items)

    def sort_keys(self, descending: bool = False) -> Self:
        sorted_items = self._sort_items(
            self.all(), key=lambda item: str(item[0]), descending=descending
        )

        return self.__class__(sorted_items)

    def _sort_items(
        self,
        items: List[Tuple[Any, Any]],
        key: Optional[Callable[[Tuple[Any, Any]], Any]] = None,
        descending: bool = False,
    ) -> Dict[Any, Any]:
        return dict(sorted(items, key=key, reverse=descending))

    def _get_iterable_items(self, data: Any) -> Dict[Any, Any]:
        try:
            if isinstance(data, Collection):
                return data._items
            elif (
                isinstance(data, list)
                and len(data)
                and all([isinstance(item, tuple) and len(item) == 2 for item in data])
            ):
                return dict(data)
            elif isinstance(data, (list, tuple)):
                return {key: item for key, item in enumerate(data)}
            elif isinstance(data, dict):
                return data
            else:
                return {0: data}
        except Exception as e:
            raise Exception("Invalid Items passed to collection")
