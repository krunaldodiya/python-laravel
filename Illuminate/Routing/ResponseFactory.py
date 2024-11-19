from typing import TYPE_CHECKING, Any, Type

from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable
from Illuminate.Support.Facades.Event import Event

if TYPE_CHECKING:
    from Illuminate.Foundation.Application import Application


class ResponseFactory:
    def __init__(self, app: Type["Application"]) -> None:
        self.__app = app

        self.__content = ""
        self.__status = "200 OK"
        self.__headers = {"Content-type": "text/plain"}

    def get_status_code(self):
        return self.__status

    def get_headers(self):
        return [(key, value) for key, value in self.__headers.items()]

    def get_content(self):
        return self.__content

    def set_content(self, content: str):
        self.__content = content

        return self

    def set_status(self, status: str):
        self.__status = status

        return self

    def set_headers(self, key: str, value: Any):
        self.__headers[key] = value

        return self

    def send(self):
        Event.dispatch("response_sent", {"response": self})

        return self

    @classmethod
    def serialize(cls, data):
        if isinstance(data, JsonSerializable):
            return cls.serialize(data.json_serialize())
        elif (
            isinstance(data, list)
            and len(data)
            and all([isinstance(item, tuple) and len(item) == 2 for item in data])
        ):
            if all([isinstance(item[0], int) for item in data]):
                return cls.serialize(list(dict(data).values()))
            else:
                return cls.serialize(dict(data))
        elif isinstance(data, (list, tuple)):
            return [cls.serialize(item) for item in data]
        elif isinstance(data, (dict, set)):
            return {key: cls.serialize(value) for key, value in data.items()}
        else:
            return data
