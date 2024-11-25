import re

from typing import Any
from Illuminate.Contracts.Container.Container import Container


class HandleCors:
    def __init__(self, container: Container) -> None:
        self.__container = container

    def handle(self, request, next) -> Any:
        config = self.__container.make("config")

        cors = config.get("cors", {})

        full_url = request.get_full_url()

        if not self.has_matching_path(cors, full_url):
            return next(request)

        return next(request)

    def has_matching_path(self, cors, full_url):
        paths = self.get_path_by_hosts(cors)

        for path in paths:
            return self.validate_path(full_url, path)

        return False

    def get_path_by_hosts(self, cors):
        return cors.get("paths")

    def validate_path(self, full_url, path):
        escaped_pattern = re.escape(path)
        regex_pattern = escaped_pattern.replace(r"\*", r".*")

        if re.search(regex_pattern, full_url):
            return True
        else:
            return False
