import abc

from typing import Any, Dict, List, Literal, TYPE_CHECKING, Tuple, Union

from Illuminate.Collections.helpers import collect
from Illuminate.Validation.helpers import pascal_to_snake

if TYPE_CHECKING:
    from Illuminate.Validation.RulesMapper import RulesMapper


class Rule(abc.ABC):
    def __init__(self, *args, **kwargs) -> None:
        self.__args = collect(args)
        self.__kwargs = kwargs

        self.__params: dict = {}
        self.__data: dict = {}
        self.__rule_type: Literal["string", "object"] | None = None
        self.__rules_mapper: "RulesMapper" | None = None

    @property
    def args(self):
        return self.__args

    @property
    def kwargs(self):
        return self.__kwargs

    @property
    def rule_type(self):
        return self.__rule_type

    @property
    def params(self):
        return self.__params

    @property
    def data(self):
        return self.__data

    @property
    def rules_mapper(self):
        return self.__rules_mapper

    @property
    def rule_name(self):
        return pascal_to_snake(self.__class__.__name__)

    @abc.abstractmethod
    def validate(self):
        raise NotImplementedError

    def get_message(self):
        return None

    def get_formatted_message(
        self,
        rule_item: str,
        messages: Dict[str, str],
        data: Dict[str, str],
    ):
        field = self.params.get("field")

        if f"{field}.{rule_item}" in messages:
            message = messages[f"{field}.{rule_item}"]
        elif field in messages:
            message = messages[field]
        else:
            message = self.get_message()

        return self.__format_template_message(message)

    def __format_template_message(self, template: str) -> str:
        for key, value in self.params.items():
            placeholder = f"{{{key}}}"

            template = template.replace(placeholder, str(value))

        return template

    def set_meta(
        self,
        rules_mapper: "RulesMapper",
        rule_type: Literal["string", "object"],
        data: Dict[str, Any],
    ):
        self.__rules_mapper = rules_mapper
        self.__rule_type = rule_type
        self.__data = data

        return self

    def require_params_count(self, count):
        if len(self.args) < count:
            raise Exception(
                f"Validation rule {self.rule_name} requires at least {count} parameters."
            )

    def set_params(self, params):
        self.__params.update(params)

        return self

    def is_validatable(self, field: str, rule_item: str) -> bool:
        present = self.check_present_or_implicit(field, rule_item)

        nullable = self.is_not_null_if_marked_as_nullable(field, rule_item)

        optional = self.passes_optional_check(field, rule_item)

        return present and nullable and optional

    def is_implicit_rule(self, field: str, rule_item: str):
        return rule_item in self.rules_mapper.implicit_rules

    def check_present_or_implicit(self, field: str, rule_item: str):
        field_exists = self.field_exists(field)

        return field_exists or self.is_implicit_rule(field, rule_item)

    def is_not_null_if_marked_as_nullable(self, field: str, rule_item: str):
        is_implicit = self.is_implicit_rule(field, rule_item)

        has_nullable = self.has_rule(field, ["nullable"])

        return is_implicit or not has_nullable

    def passes_optional_check(self, field: str, rule_item: str):
        has_sometimes = self.has_rule(field, ["sometimes"])

        if not has_sometimes:
            return True

        return self.field_exists(field)

    def field_exists(self, field: str):
        try:
            self.data[field]

            return True
        except KeyError:
            return False

    def value_exists(self, value: str):
        return self.is_countable(value) and len(value) > 0

    def has_rule(self, field: str, rules: List[str]) -> bool:
        field_rules = self.get_field_rules(field)

        return all(rule in field_rules for rule in rules)

    def get_field_rules(self, field: str) -> list:
        rules = self.rules_mapper.rules[field]

        return list(rules.keys())

    def get_size(self) -> int | float | None:
        field = self.params.get("field")

        value = self.params.get("value")

        has_numeric = self.has_rule(field, ["numeric"])

        is_numeric, numeric_value = self.is_numeric_value(value)

        self.is_numeric = is_numeric and has_numeric

        if self.is_numeric:
            return numeric_value
        elif isinstance(value, list):
            return len(value)
        else:
            return len(str(value))

    def is_numeric_value(self, value: Any) -> Tuple[bool, Union[int | float | None]]:
        if isinstance(value, (int, float)):
            return True, value

        if isinstance(value, str):
            try:
                return True, float(value)
            except ValueError:
                return False, None

        return False, None

    def is_countable(self, value) -> bool:
        return isinstance(value, (list, tuple, dict, set, range, str, bytes))
