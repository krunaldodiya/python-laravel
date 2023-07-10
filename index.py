from core.application import Application
from core.controller import Controller
from core.file_loader import load_files


load_files("app/Http/Controllers")
load_files("app/routes")


application = Application()

for controller in Controller.__subclasses__():
    application.bind(controller.__name__, controller)

test = application.resolve(controller.__name__)

application.boot()

application.run()
