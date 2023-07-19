import os
from pathlib import Path
from typing import TYPE_CHECKING, Type
from dotenv import load_dotenv

if TYPE_CHECKING:
    from Illuminate.Foundation.Application import Application


class LoadEnvironmentVariables:
    def bootstrap(self, app: Type["Application"]) -> None:
        self.__load_environment(".env", False)

        if os.getenv("APP_ENV"):
            self.__load_environment(f".env." + os.getenv("APP_ENV"), True)

    def __load_environment(self, environment, override):
        env_path = Path(environment)

        load_dotenv(env_path, override=override)
