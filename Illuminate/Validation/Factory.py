from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Validation.Validator import Validator


class Factory:
    def __init__(self, app: Application):
        self.__app = app

    def make(self, data, rules, messages=[], attributes=[]) -> Validator:
        validator = self._resolve(data, rules, messages, attributes)

        if self.__app:
            validator.set_application(self.__app)

        return validator

    def validate(self, data, rules, messages=[], attributes=[]):
        return self.make(data, rules, messages, attributes).validate()

    def _resolve(self, data, rules, messages=[], attributes=[]) -> Validator:
        return Validator(data, rules, messages, attributes)
