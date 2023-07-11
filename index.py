from core.Support.Facades.Facade import Facade
from core.application import Application
from core.controller import Controller
from core.file_loader import load_files
from core.router import Router


load_files("app/Http/Controllers")
load_files("routes")


if __name__ == "__main__":
    application = Application()

    for controller in Controller.__subclasses__():
        application.bind(controller.__name__, controller)

    application.bind("router", lambda: Router())

    application.run()
