import os
from pathlib import Path
from typing import TYPE_CHECKING, Type
from dotenv import load_dotenv

if TYPE_CHECKING:
    from Illuminate.Foundation.Application import Application


class LoadEnvironmentVariables:
    def bootstrap(self, app: Type["Application"]) -> None:
        environment_file_path = app.environment_file_path()
        self.__load_environment(environment_file_path, False)

        if os.getenv("APP_ENV"):
            env_path = f'{environment_file_path}.{os.getenv("APP_ENV")}'

            if Path(env_path).exists():
                app.load_environment_from(env_path)
                self.__load_environment(env_path, True)

    def __load_environment(self, env_path, override):
        load_dotenv(env_path, override=override)
