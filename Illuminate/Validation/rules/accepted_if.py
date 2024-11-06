from Illuminate.Validation.Rule import Rule


class AcceptedIf(Rule):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.accepts = ["yes", "on", 1, "1", True, "true"]

    def validate(self) -> bool:
        self.require_params_count(2)

        self.set_params(
            {"required_if_key": self.args[0], "required_if_value": self.args[1]}
        )

        required_if_key = self.params.get("required_if_key")

        required_if_value = self.params.get("required_if_value")

        expression = f"'{self.data.get(required_if_key)}' == {repr(required_if_value)}"

        status = eval(expression)

        if status:
            value = self.params.get("value")

            if self.value_exists(value):
                return value in self.accepts

            return False

        return True

    def get_message(self) -> str:
        return "{field} is required when {required_if_key} is {required_if_value}"
