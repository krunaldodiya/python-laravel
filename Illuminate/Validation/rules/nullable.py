from Illuminate.Validation.Rule import Rule


class Nullable(Rule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self):
        self.require_params_count(0)

        return True
