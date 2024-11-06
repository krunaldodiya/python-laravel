import re

from Illuminate.Validation.Rule import Rule


class Email(Rule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    def validate(self):
        self.require_params_count(0)

        value = self.params.get("value")

        if not value or not re.match(self.email_regex, str(value)):
            return False

        return True

    def get_message(self):
        return "The {field} must be a valid email address."
