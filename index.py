from core.Support.Foundation.Application import Application
from core.file_loader import load_files

if __name__ == "__main__":
    application = Application()

    application.register_providers()
    application.register_facades()

    load_files("routes")
    load_files("app/Http/Controllers")

    application.run()
