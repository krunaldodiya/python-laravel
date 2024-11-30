from enum import Enum


class InputOption(Enum):
    VALUE_NONE = 1
    VALUE_REQUIRED = 2
    VALUE_OPTIONAL = 4
    VALUE_IS_ARRAY = 8
