from core.Support.Foundation.Application import Application
from core.Support.Facades.Route import Route
from core.file_loader import load_files

if __name__ == "__main__":
    application = Application()

    application.register_providers()

    Route.app = application

    load_files("app/Http/Controllers")
    load_files("routes")

    application.run()
