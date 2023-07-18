from typing import Any


class HandleCors:
    def handle(self, passable, next) -> Any:
        print("handling cors")
