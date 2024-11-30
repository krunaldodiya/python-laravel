from typing import Any, Callable, List, Self
from Illuminate.Collections.Enumerable import Enumerable
from Illuminate.Collections.helpers import data_get

from Illuminate.Conditionable.Conditionable import Conditionable
from Illuminate.Helpers.Util import Util
from Illuminate.Routing.ResponseFactory import ResponseFactory
from Illuminate.Support.helpers import safe_eval_compare


class EnumeratesValues(Conditionable, Enumerable):
    def __getitem__(self, index):
        return self._items[index]

    def __setitem__(self, index, value):
        self._items[index] = value

    def __delitem__(self, index):
        del self._items[index]

    def __iter__(self):
        return iter(self.all())

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.json_serialize()})"

    def is_listable(self) -> bool:
        return all([isinstance(item, int) for item in self._items])

    def to_list(self) -> List[Any]:
        return list(self._items.values())

    def map_into(self, class_name) -> Self:
        return self.map(lambda value, key: class_name(value, key))

    def reject(self, callback=True) -> Self:
        return self.filter(
            lambda value, key: (
                not Util.callback_with_dynamic_args(callback, [value, key])
                if callable(callback)
                else self._bool_value(value) != self._bool_value(callback)
            )
        )

    def each(self, callback: Callable[[Any], Any]) -> Self:
        self._check_is_callable(callback)

        for key, value in self:
            status = Util.callback_with_dynamic_args(callback, [value, key])

            if status == False:
                break

        return self

    def every(self, data_key, data_operator=None, data_value=None) -> bool:
        if not data_operator and not data_value:
            self._check_is_callable(data_key)

            callback = self._value_retriever(data_key)

            for key, value in self:
                status = Util.callback_with_dynamic_args(callback, [value, key])

                if self._bool_value(status) == False:
                    return False

            return True

        return self.every(
            lambda value: safe_eval_compare(
                data_get(value, data_key), data_operator, data_value
            )
        )

    def where_instance_of(self, instance: Any) -> Self:
        return self.filter(lambda item: isinstance(item, instance))

    def partition(self, data_key, data_operator=None, data_value=None):
        passed = {}
        failed = {}

        if not data_operator and not data_value:
            self._check_is_callable(data_key)

            callback = self._value_retriever(data_key)

            for key, value in self:
                if Util.callback_with_dynamic_args(callback, [value, key]):
                    passed[key] = value
                else:
                    failed[key] = value

            return [self.__class__(passed), self.__class__(failed)]

        return self.partition(
            lambda value: safe_eval_compare(
                data_get(value, data_key), data_operator, data_value
            )
        )

    def json_serialize(self) -> Any:
        return ResponseFactory.serialize(
            self.to_list() if self.is_listable() else self._items
        )

    def _bool_value(self, value):
        return True if value else False

    def _value_retriever(self, value):
        if callable(value):
            return value

        return lambda item: data_get(item, value)

    def _check_is_callable(self, callback: Any) -> None:
        if not callable(callback):
            raise ValueError("Expected a callable")

    def _get_key(self):
        if not self.count():
            return 0

        keys = [key for key in self._items.keys() if isinstance(key, int)]

        if keys:
            return max(keys) + 1

        return 0
