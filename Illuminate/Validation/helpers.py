import re


def snake_to_pascal(rule_name):
    """Converts snake_case to PascalCase."""
    return "".join(word.capitalize() for word in rule_name.split("_"))


def pascal_to_snake(class_name):
    """Converts PascalCase to snake_case."""
    snake_case = re.sub(r"(?<!^)(?=[A-Z])", "_", class_name).lower()

    return snake_case
