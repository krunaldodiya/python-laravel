import re


def validate_path(full_url, path):
    escaped_pattern = re.escape(path)
    regex_pattern = escaped_pattern.replace(r"\*", r".*")

    if re.search(regex_pattern, full_url):
        return True
    else:
        return False


url = "http://google.com/api/test"
pattern = "api/*"

if validate_path(url, pattern):
    print("URL path matches the pattern.")
else:
    print("URL path does not match the pattern.")
