from typing import Any, Callable, List
from Illuminate.Contracts.Auth.Access.Gate import Gate as GateContract


class Gate(GateContract):
    def __init__(self, app) -> None:
        self.__app = app

        self.__abilities = {}

    def define(self, ability: str, callback: Callable[[Any], Any]):
        self.__abilities[ability] = callback

    def check(self, ability: str, arguments: List[Any]) -> bool:
        abilities = [ability] if isinstance(ability, str) else ability

        return all(
            self.__abilities.get(ability, lambda *args: False)(*arguments)
            for ability in abilities
        )
