from Illuminate.Helpers.to_dict import to_dict


class HeaderBag:
    def __init__(self, headers) -> None:
        self.headers = {
            key.decode("utf-8"): value.decode("utf-8") for key, value in headers
        }

        self.cache_controller = {
            "cache-control": to_dict(self.headers.get("cache-control", "max-age=0"))
        }
