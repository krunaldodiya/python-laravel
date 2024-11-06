from typing import Any, Dict, List, Self


class ValidationResponse:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.__initial_data = data
        self.__validated_data: dict = {}
        self.__validation_errors: dict = {}
        self.__validated = False

    @property
    def validated(self) -> bool:
        return self.__validated

    @property
    def data(self) -> Dict[str, Any]:
        return self.__validated_data

    @property
    def errors(self) -> Dict[str, List[str]]:
        return self.__validation_errors

    def set_error(self, field, value) -> None:
        field_errors = self.__validation_errors.setdefault(field, [])

        field_errors.append(value)

    def execute(self) -> Self:
        self.__validated = len(self.errors.keys()) == 0

        if self.__validated:
            self.__validated_data = self.__initial_data

        return self
