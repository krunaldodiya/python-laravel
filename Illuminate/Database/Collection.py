import inspect

from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Self,
    Tuple,
    TypeVar,
    Union,
)

from Illuminate.Database.Serializable import Serializable

T = TypeVar("T")


class Collection(Serializable, Generic[T]):
    def __init__(self, items=[]) -> None:
        super().__init__([])

        self.items = self._get_iterable_items(items)

    def filter(self, callback: Optional[Callable[[Any], Any]] = None) -> Self:
        if not callback:
            return self.__class__(self.items)

        self._check_is_callable(callback)

        args_count = self._get_callback_arg_count(callback)

        results = [
            (key, value)
            for key, value in self.items
            if callback(*self._build_args(key, value, args_count))
        ]

        return self.__class__(results)

    def map(self, callback: Callable[[Any], Any]) -> Self:
        self._check_is_callable(callback)

        args_count = self._get_callback_arg_count(callback)

        results = [
            (key, callback(*self._build_args(key, value, args_count)))
            for key, value in self.items
        ]

        return self.__class__(results)

    def group_by(self, callback_or_string: Union[Callable[[Any], Any], str]):
        if callable(callback_or_string):
            self._check_is_callable(callback_or_string)
            group_callback = callback_or_string

        if isinstance(callback_or_string, str):
            group_callback = lambda item: (
                item.get(callback_or_string, "")
                if isinstance(item, dict)
                else getattr(item, callback_or_string, "")
            )

        args_count = self._get_callback_arg_count(group_callback)

        results = {}

        for key, value in self.items:
            args = self._build_args(key, value, args_count)

            def get_group_key(group_callback, args):
                try:
                    return group_callback(*args)
                except:
                    return ""

            group_key = get_group_key(group_callback, args)

            results.setdefault(group_key, self.__class__([])).push(value)

        return self.__class__([(key, items) for key, items in results.items()])

    def sort_by(
        self,
        callback_or_string: Union[Callable[[Any], Any], str],
        descending: bool = False,
    ):
        if callable(callback_or_string):
            self._check_is_callable(callback_or_string)
            sort_callback = callback_or_string

        if isinstance(callback_or_string, str):
            sort_callback = lambda item: (
                item.get(callback_or_string, "")
                if isinstance(item, dict)
                else getattr(item, callback_or_string, "")
            )

        args_count = self._get_callback_arg_count(sort_callback)

        if args_count == 2:
            sort_key = lambda item: sort_callback(item[1], item[0])
        else:
            sort_key = lambda item: sort_callback(item[1])

        data = sorted(self.items, key=sort_key, reverse=descending)

        return self.__class__([(key, items) for key, items in data])

    def sort(
        self,
        sort_callback: Optional[Callable[[Any], Any]] = None,
        descending: bool = True,
    ):
        if sort_callback:
            self._check_is_callable(sort_callback)

            return self.sort_by(sort_callback, descending)

        sort_callback = lambda item, key: key

        return self.sort_by(sort_callback, descending)

    def sort_keys(
        self,
        sort_callback: Optional[Callable[[Any], Any]] = None,
        descending: bool = False,
    ):
        if sort_callback:
            self._check_is_callable(sort_callback)

            return self.sort_by(sort_callback, descending)

        sort_callback = lambda item, key: key

        return self.sort_by(sort_callback, descending)

    def first(self, callback: Optional[Callable[[Any], bool]] = None) -> Any:
        items = self.items

        if callback:
            items = self.filter(callback)

        return items[0][1] if items else None

    def last(self, callback: Optional[Callable[[Any], bool]] = None) -> Any:
        items = list(reversed(self.items))

        if callback:
            items = self.filter(callback)

        return items[0][1] if items else None

    def count(self) -> List[Any]:
        return len(self.items)

    def all(self) -> Dict:
        return self.items

    def to_list(self) -> List[Any]:
        return [item for _, item in self.items]

    def to_dict(self) -> Dict[Any, Any]:
        return dict(self.items)

    def to_base(self) -> Self:
        return Collection(self.items)

    def values(self) -> Self:
        return self.__class__(self.to_list())

    def push(self, item) -> Self:
        key = self._get_key()

        self.items.append((key, item))

        return self

    def flatten(self, depth: int = -1) -> Self:
        flattened_items = self._flatten([value for _, value in self.items], 0, depth)

        return self.__class__(flattened_items)

    def _build_args(self, key, value, args_count):
        return [value, key] if args_count == 2 else [value]

    def _check_is_callable(self, callback: Any) -> None:
        if not callable(callback):
            raise ValueError("Expected a callable")

    def _get_callback_arg_count(self, callback: Callable) -> int:
        sig = inspect.signature(callback)

        args = [
            p
            for p in sig.parameters.values()
            if p.kind in (p.POSITIONAL_OR_KEYWORD, p.POSITIONAL_ONLY)
        ]

        return len(args)

    def _get_iterable_items(self, items: Any) -> List:
        if isinstance(items, Collection):
            return items.items

        if isinstance(items, List):
            if all(isinstance(item, Tuple) for item in items):
                return items
            else:
                return [(key, item) for key, item in enumerate(items)]

        if isinstance(items, Dict):
            return [(key, item) for key, item in items.items()]

        if isinstance(items, Tuple):
            return [items]

        return [(0, items)]

    def _get_key(self):
        if not self.count():
            return 0

        keys = [key for key, _ in self.items if isinstance(key, int)]

        if keys:
            return max(keys) + 1

        return 0

    def _flatten(self, items: Any, current_depth: int, depth: int) -> List[Any]:
        if not isinstance(items, (list, tuple, dict)) or (depth == 0):
            return [items]

        flattened = []

        for item in items:
            if isinstance(item, (list, tuple, dict)) and (
                depth == -1 or current_depth < depth
            ):
                if isinstance(item, dict):
                    flattened.extend(
                        self._flatten(list(item.values()), current_depth + 1, depth)
                    )
                else:
                    flattened.extend(self._flatten(item, current_depth + 1, depth))
            else:
                flattened.append(item)

        return flattened
