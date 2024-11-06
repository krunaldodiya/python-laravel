from Illuminate.Validation.Rule import Rule


class Required(Rule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self):
        self.require_params_count(0)

        value = self.params.get("value")

        return self.value_exists(value)

    def get_message(self):
        return "The {field} field is required"
