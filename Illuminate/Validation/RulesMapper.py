import importlib
import os

from typing import Any, Dict, List, Type
from Illuminate.Validation.Rule import Rule
from Illuminate.Validation.helpers import snake_to_pascal


class RulesMapper:
    def __init__(self) -> None:
        self.__rule_executor_types: Dict[str, Type[Rule]] = (
            self.__get_rule_executor_types()
        )

        self.__rules: dict[str, Dict[str, Rule]] = {}

        self.__implicit_rules = [
            "accepted",
            "accepted_if",
            "declined",
            "declined_if",
            "filled",
            "missing",
            "missing_if",
            "missing_unless",
            "missing_with",
            "missing_with_all",
            "present",
            "present_if",
            "present_unless",
            "present_with",
            "present_with_all",
            "required",
            "required_if",
            "required_if_accepted",
            "required_if_declined",
            "required_unless",
            "required_with",
            "required_with_all",
            "required_without",
            "required_without_all",
        ]

        self.__dependent_rules = [
            "after",
            "after_or_equal",
            "before",
            "before_or_equal",
            "confirmed",
            "different",
            "exclude_if",
            "exclude_unless",
            "exclude_with",
            "exclude_without",
            "gt",
            "gte",
            "lt",
            "lte",
            "accepted_if",
            "declined_if",
            "required_if",
            "required_if_accepted",
            "required_if_declined",
            "required_unless",
            "required_with",
            "required_with_all",
            "required_without",
            "required_without_all",
            "present_if",
            "present_unless",
            "present_with",
            "present_with_all",
            "prohibited",
            "prohibited_if",
            "prohibited_unless",
            "prohibits",
            "missing_if",
            "missing_unless",
            "missing_with",
            "missing_with_all",
            "same",
            "unique",
        ]

        self.__exclude_rules = [
            "exclude",
            "exclude_if",
            "exclude_unless",
            "exclude_with",
            "exclude_without",
        ]

        self.size_rules = [
            "between",
            "max",
            "min",
            "size",
            "gt",
            "lt",
            "gte",
            "lte",
        ]

        self.__numeric_rules = [
            "numeric",
            "integer",
            "decimal",
        ]

        self._initialized = True

    @property
    def rule_executor_types(self):
        return self.__rule_executor_types

    @property
    def rules(self):
        return self.__rules

    @property
    def implicit_rules(self):
        return self.__implicit_rules

    def __get_listable_rules(
        self, rules: Dict[str, str | List[Any]]
    ) -> Dict[str, List[Any]]:
        formatted_rules = {}

        for field, rule_item in rules.items():
            if isinstance(rule_item, str):
                formatted_rules[field] = rule_item.split("|")
            else:
                formatted_rules[field] = rule_item

        return formatted_rules

    def __get_rule_executor_types(self):
        rules_directory = os.path.join(os.path.dirname(__file__), "rules")

        rule_executor_types = {}

        for filename in os.listdir(rules_directory):
            if filename.endswith(".py") and filename != "__init__.py":
                rule_name = filename[:-3]

                class_name = snake_to_pascal(rule_name)

                try:
                    module = importlib.import_module(
                        f"Illuminate.Validation.rules.{rule_name}"
                    )

                    rule_class = getattr(module, class_name)

                    rule_executor_types[rule_name] = rule_class
                except (ImportError, AttributeError) as e:
                    print(f"Failed to load rule '{rule_name}': {e}")

        return rule_executor_types

    def set_rules(self, rules: Dict[str, List[Any]], data: Dict[str, Any]) -> None:
        listable_rules = self.__get_listable_rules(rules)

        for field, rule_items in listable_rules.items():
            value = data.get(field, None)

            params = {"field": field, "value": value}

            for rule_item in rule_items:
                rule_item_instance = None

                if isinstance(rule_item, Rule):
                    rule_item_instance = rule_item
                    rule_item_instance.set_meta(self, "object", data).set_params(params)

                if isinstance(rule_item, str):
                    rule_item_instance = self.__get_rule_executor(rule_item)
                    rule_item_instance.set_meta(self, "string", data).set_params(params)

                if not rule_item_instance:
                    raise Exception("Invalid Rule")

                self.__set_rule_executor(field, rule_item_instance)

    def __set_rule_executor(self, field: str, rule_item_instance: Rule) -> None:
        if field not in self.rules:
            self.rules[field] = {}

        rule_name = rule_item_instance.rule_name

        self.rules[field][rule_name] = rule_item_instance

    def __get_rule_executor(self, rule_item: str) -> Rule:
        try:
            rule_with_args = rule_item.split(":")

            rule = rule_with_args[0]

            rule_args = None if len(rule_with_args) == 1 else rule_with_args[1]

            rule_args = rule_args.split(",") if rule_args else []

            rule_executor_type = self.__rule_executor_types[rule]

            return rule_executor_type(*rule_args)
        except KeyError:
            raise Exception(f"Rule `{rule}` does not exists.")
