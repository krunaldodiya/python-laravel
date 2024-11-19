from typing import Any, Dict, List, Union
from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Validation.Rule import Rule
from Illuminate.Validation.RulesMapper import RulesMapper
from Illuminate.Validation.ValidationResponse import ValidationResponse


class Validator:
    def __init__(
        self,
        data: Dict[str, Any],
        rules: Dict[str, List[Union[str | Rule]]],
        messages: Dict[str, Any] | None = None,
        attributes: Dict[str, Any] | None = None,
    ):
        self.data = data

        self.rules = rules

        self.messages = messages or {}

        self.attributes = attributes or {}

        self.__validate_payload()

        self.validation_response = ValidationResponse(self.data)

        self.rules_mapper = RulesMapper()

        self.rules_mapper.set_rules(self.rules, self.data)

    def set_application(self, app: Application):
        self.__app = app

    def validate(self) -> ValidationResponse:
        try:
            for field, rules in self.rules_mapper.rules.items():
                for rule_item, rule_executor in rules.items():
                    validatable = rule_executor.is_validatable(field, rule_item)

                    if validatable:
                        should_process_next = self.__process_validation(
                            field,
                            rule_item,
                            rule_executor,
                            self.messages,
                            self.data,
                        )

                        if not should_process_next:
                            break

            return self.validation_response.execute()
        except Exception as e:
            raise Exception(str(e))

    def __process_validation(
        self,
        field: str,
        rule_item: str,
        rule_executor: Rule,
        messages: Dict[str, Any],
        data: Dict[str, Any],
    ):
        validated = rule_executor.validate()

        if not validated:
            formatted_message = rule_executor.get_formatted_message(
                rule_item, messages, data
            )

            self.validation_response.set_error(
                rule_executor.params.get("field"), formatted_message
            )

            if rule_item in self.rules_mapper.implicit_rules:
                return False

        return True

    def get_params(self, field_name: str, rule_name: str) -> Dict[str, Any]:
        params = {}

        for field, rules in self.rules_mapper.rules.items():
            for rule, executor in rules.items():
                if field == field_name and rule == rule_name:
                    params = executor.params

        return params

    def __validate_payload(self):
        assert isinstance(self.data, dict), "Data is not a dictionary"

        assert isinstance(self.messages, dict), "Messages is not a dictionary"

        assert isinstance(self.rules, dict), "Field rule items is not a dictionary"

        assert all(
            all(isinstance(item, (str, Rule)) for item in value)
            for value in self.rules.values()
        ), "Not all items in lists are strings or instances of Rule"
