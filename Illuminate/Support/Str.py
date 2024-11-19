import random
import re
import string
import unicodedata

from pluralizer import Pluralizer


class Str:
    _snake_cache = {}
    _kebab_cache = {}
    _camel_cache = {}
    _pascal_cache = {}
    _plural_cache = {}
    _singular_cache = {}
    _pluralizer = None

    @classmethod
    def random(cls, length=32) -> str:
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    @classmethod
    def contains(cls, haystack, needles):
        if not haystack or not needles:
            return False

        return any(needle in haystack for needle in needles)

    @classmethod
    def get_pluralizer(cls):
        if not Str._pluralizer:
            Str._pluralizer = Pluralizer()

        return Str._pluralizer

    @classmethod
    def plural(cls, word):
        """Convert a word to its plural form using inflect library."""
        if word in Str._plural_cache:
            return Str._plural_cache[word]

        plural_form = Str.get_pluralizer().plural(word)
        Str._plural_cache[word] = plural_form
        return plural_form

    @classmethod
    def singular(cls, word):
        """Convert a word to its singular form using inflect library."""
        if word in Str._singular_cache:
            return Str._singular_cache[word]

        singular_form = Str.get_pluralizer().singular(word) or word
        Str._singular_cache[word] = singular_form
        return singular_form

    @classmethod
    def _normalize_and_clean(cls, string):
        """Normalize and clean a string for processing."""
        normalized_string = (
            unicodedata.normalize("NFKD", string)
            .encode("ascii", "ignore")
            .decode("utf-8")
        )
        cleaned_string = re.sub(r"[^a-z0-9\s]", "", normalized_string.lower())
        return cleaned_string

    @classmethod
    def snake(cls, value, delimiter="_"):
        """Convert a string to snake_case with a customizable delimiter."""
        if (cache := Str._snake_cache.get(value)) and delimiter in cache:
            return cache[delimiter]

        value = re.sub(
            r"(?<!^)(?=[A-Z])", " ", value
        )  # Add space before uppercase letters
        value = value.replace(" ", delimiter)
        result = value.lower()
        Str._snake_cache.setdefault(value, {})[delimiter] = result
        return result

    @classmethod
    def kebab(cls, value):
        """Convert a string to kebab-case."""
        if value in Str._kebab_cache:
            return Str._kebab_cache[value]

        result = Str.snake(value, "-")
        Str._kebab_cache[value] = result
        return result

    @classmethod
    def camel(cls, value):
        """Convert a string to camelCase."""
        if value in Str._camel_cache:
            return Str._camel_cache[value]

        words = re.findall(r"[A-Z][a-z]*|[a-z]+", value)
        result = (
            words[0].lower() + "".join(word.capitalize() for word in words[1:])
            if words
            else value
        )
        Str._camel_cache[value] = result
        return result

    @classmethod
    def pascal(cls, value):
        """Convert a string to PascalCase."""
        if value in Str._pascal_cache:
            return Str._pascal_cache[value]

        words = re.findall(r"[A-Z][a-z]*|[a-z]+", value)
        result = "".join(word.capitalize() for word in words)
        Str._pascal_cache[value] = result
        return result

    @classmethod
    def title(cls, value):
        """Convert a string to title case."""
        return value.title()

    @classmethod
    def lower(cls, value: str):
        """Convert a string to title case."""
        return value.lower()

    @classmethod
    def slug(cls, title, separator="-", language="en", dictionary={"@": "at"}):
        """Generate a URL-friendly slug from a given string."""
        title = Str._normalize_and_clean(title)
        flip = "_" if separator == "-" else "-"
        title = re.sub(rf"[{re.escape(flip)}]+", separator, title)

        for key, value in dictionary.items():
            title = title.replace(key, f"{separator}{value}{separator}")

        title = re.sub(r"[^a-z0-9\s]+", "", title.lower())
        title = re.sub(rf"[{re.escape(separator)}\s]+", separator, title)

        return title.strip(separator)
