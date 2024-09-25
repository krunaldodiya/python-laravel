import os

from pathlib import Path
from dotenv import load_dotenv
from Illuminate.Contracts.Foundation.Application import Application


class LoadEnvironmentVariables:
    def bootstrap(self, app: Application) -> None:
        environment_file_path = app.environment_file_path()
        self.__load_environment(environment_file_path, False)

        if os.getenv("APP_ENV"):
            env_path = f'{environment_file_path}.{os.getenv("APP_ENV")}'

            if Path(env_path).exists():
                app.load_environment_from(env_path)
                self.__load_environment(env_path, True)

    def __load_environment(self, env_path, override):
        load_dotenv(env_path, override=override)
