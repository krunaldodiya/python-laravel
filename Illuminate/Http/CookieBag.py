from Illuminate.Helpers.to_dict import to_dict


class CookieBag:
    def __init__(self, cookie) -> None:
        self.parameters = to_dict(cookie)
