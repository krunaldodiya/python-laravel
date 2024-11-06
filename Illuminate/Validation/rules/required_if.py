from typing import Callable
from Illuminate.Validation.Rule import Rule


class RequiredIf(Rule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self):
        status = (
            self.validate_object()
            if self.rule_type == "object"
            else self.validate_string()
        )

        if status:
            value = self.params.get("value")

            if self.value_exists(value):
                return self.value_exists(value)

        return True

    def validate_object(self) -> bool:
        self.require_params_count(1)

        self.set_params({"validator_object": self.args[0]})

        object_arg = self.args[0]

        if isinstance(object_arg, bool):
            return object_arg

        if isinstance(object_arg, Callable):
            return object_arg()

    def validate_string(self) -> bool:
        self.require_params_count(2)

        self.set_params(
            {"required_if_key": self.args[0], "required_if_value": self.args[1]}
        )

        required_if_key = self.params.get("required_if_key")

        required_if_value = self.params.get("required_if_value")

        expression = f"'{self.data.get(required_if_key)}' == {repr(required_if_value)}"

        return eval(expression)

    def get_message(self):
        if self.rule_type == "string":
            return "{field} is required when {required_if_key} is {required_if_value}"

        return "{field} is required"
