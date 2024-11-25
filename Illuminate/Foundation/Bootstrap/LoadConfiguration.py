import importlib

from Illuminate.Config.Repository import Repository
from Illuminate.Contracts.Foundation.Application import Application


class LoadConfiguration:
    def bootstrap(self, app: Application) -> None:
        self.__app = app

        config_path = self.__app.make("path.config")

        config = Repository({}, config_path)

        self.__app.instance("config", config)

        self.__load_configuration_files(config)

        self.__app.detect_environment(lambda: config.get("app.env", "production"))

    def __load_configuration_files(self, config):
        files = config.get_files()

        for file in files:
            file_name, file_content = self.__get_info(file)

            config.set(file_name, file_content)

    def __get_info(self, file):
        file_name = file.name[:-3]

        spec = importlib.util.spec_from_file_location(file_name, file)

        module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(module)

        return file_name, getattr(module, file_name)
