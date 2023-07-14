import os
from pathlib import Path
from dotenv import load_dotenv


class LoadEnvironment:
    def __init__(self, environment=None, override=True) -> None:
        env_path = Path(".env")
        load_dotenv(env_path)

        if os.environ.get("APP_ENV"):
            self.__load_environment(os.environ.get("APP_ENV"), override=override)

        if environment:
            self._load_environment(environment, override=override)

    def __load_environment(self, environment, override):
        env_path = Path(f".env.{environment}")
        load_dotenv(env_path)
