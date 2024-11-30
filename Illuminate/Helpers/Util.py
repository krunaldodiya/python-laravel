import copy
import inspect
import types

from typing import Any, Callable, Dict, List


class Util:
    @classmethod
    def to_boolean(cls, value: Any):
        try:
            return bool(value)
        except:
            return value

    @classmethod
    def convert_values_to_string(cls, data):
        copied_data = copy.copy(data)

        def converter(obj):
            if isinstance(obj, dict):
                return {key: converter(value) for key, value in obj.items()}

            elif isinstance(obj, list):
                return [converter(value) for value in obj]

            elif callable(obj):
                return obj.__module__ + "." + obj.__name__

            return str(obj)

        return converter(copied_data)

    @classmethod
    def to_dict(cls, cookie):
        cookie_dict = {}

        for pair in cookie.split(";"):
            key, value = pair.strip().split("=")

            cookie_dict[key.strip()] = value.strip()

        return cookie_dict

    @classmethod
    def is_function(cls, item):
        return isinstance(item, types.FunctionType) or (
            isinstance(item, types.LambdaType) and item.__name__ == "<lambda>"
        )

    @staticmethod
    def get_callback_args_count(callback: Callable) -> int:
        sig = inspect.signature(callback)

        args = [
            p
            for p in sig.parameters.values()
            if p.kind in (p.POSITIONAL_OR_KEYWORD, p.POSITIONAL_ONLY)
        ]

        return len(args)

    @classmethod
    def callback_with_dynamic_args(
        cls, callback: Callable, args: List[Any] = [], kwargs: Dict[Any, Any] = {}
    ):
        try:
            args_count = cls.get_callback_args_count(callback)

            if not isinstance(args, list):
                raise Exception("Invalid args type, must be list of arguments")

            if args_count > len(args):
                raise Exception("Invalid arguments passed")

            build_args = args[:args_count]

            return callback(*build_args)
        except Exception as e:
            print(e)
