import operator
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
from Illuminate.Helpers.Util import Util

T = TypeVar("T")


class Collection(Serializable, Generic[T]):
    def __init__(self, items=[]) -> None:
        super().__init__([])

        self.items = self._get_iterable_items(items)

    def filter(self, callback: Optional[Callable[[Any], Any]] = None) -> Self:
        if not callback:
            return self.__class__([(key, value) for key, value in self.items if value])

        self._check_is_callable(callback)

        results = [
            (key, value)
            for key, value in self.items
            if Util.callback_with_dynamic_args(callback, [value, key])
        ]

        return self.__class__(results)

    def map(self, callback: Callable[[Any], Any]) -> Self:
        self._check_is_callable(callback)

        results = [
            (key, Util.callback_with_dynamic_args(callback, [value, key]))
            for key, value in self.items
        ]

        return self.__class__(results)

    def each(self, callback: Callable[[Any], Any]) -> Self:
        self._check_is_callable(callback)

        for key, value in self.items:
            status = Util.callback_with_dynamic_args(callback, [value, key])

            if status == False:
                break

        return self

    def unique(self, unique_key_callback: Callable) -> Self:
        unique_ids = []

        def is_unique(value, key):
            id = Util.callback_with_dynamic_args(unique_key_callback, [value, key])

            if id in unique_ids:
                return False

            unique_ids.append(id)

            return True

        return self.filter(lambda value, key: is_unique(value, key))

    def transform(self, callback: Callable[[Any], Any]) -> Self:
        self.items = self.map(callback).all()

        return self

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

        results = {}

        for key, value in self.items:
            group_key = Util.callback_with_dynamic_args(group_callback, [value, key])

            results.setdefault(group_key or "", self.__class__([])).push(value)

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

        sort_key = lambda item: Util.callback_with_dynamic_args(
            sort_callback, [item[1], item[0]]
        )

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

    def partition(
        self, partition_key, partition_operator=None, partition_value=None
    ) -> Tuple[Self, Self]:
        passed = {}
        failed = {}

        callback = (
            partition_key
            if Util.is_function(partition_key)
            else lambda value: self._safe_eval(
                getattr(value), partition_operator, partition_value
            )
        )

        for key, value in self.items:
            if Util.callback_with_dynamic_args(callback, [value, key]):
                passed[key] = value
            else:
                failed[key] = value

        return [self.__class__(passed), self.__class__(failed)]

    def concat(self, items) -> Self:
        results = self.__class__(self.items)

        for _, item in items:
            results.push(item)

        return results

    def to_list(self) -> List[Any]:
        return [item for _, item in self.items]

    def to_dict(self) -> Dict[Any, Any]:
        return dict(self.items)

    def to_base(self) -> Self:
        return Collection(self.items)

    def values(self) -> Self:
        return self.__class__([value for _, value in self.items])

    def push(self, item) -> Self:
        key = self._get_key()

        self.items.append((key, item))

        return self

    def flatten(self, depth: int = -1) -> Self:
        flattened_items = self._flatten(self.items, 0, depth)

        return self.__class__(flattened_items)

    def _build_args(self, key, value, args_count):
        return [value, key] if args_count == 2 else [value]

    def _check_is_callable(self, callback: Any) -> None:
        if not callable(callback):
            raise ValueError("Expected a callable")

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

    def _flatten(
        self, items: List[Tuple[Any, Any]], current_depth: int, depth: int
    ) -> List[Tuple[Any, Any]]:
        flattened = []

        for key, item in items:
            if isinstance(item, (list, Collection)) and (
                depth == -1 or current_depth < depth
            ):
                if isinstance(item, list):
                    flattened.extend(
                        self._flatten(enumerate(item), current_depth + 1, depth)
                    )
                else:
                    flattened.extend(
                        self._flatten(item.items, current_depth + 1, depth)
                    )
            else:
                flattened.append(item)

        return flattened

    def _safe_eval(self, key, oper, value):
        ops = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
            "%": operator.mod,
            "**": operator.pow,
            "==": operator.eq,
        }

        if oper in ops:
            return eval(key, ops[oper], value)
        else:
            raise ValueError("Invalid operator")
