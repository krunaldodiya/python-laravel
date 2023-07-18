def to_dict(cookie):
    cookie_dict = {}

    for pair in cookie.split(";"):
        key, value = pair.strip().split("=")

        cookie_dict[key.strip()] = value.strip()

    return cookie_dict
