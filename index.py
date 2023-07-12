from Illuminate.Support.Foundation.Application import Application
from Illuminate.file_loader import load_files

if __name__ == "__main__":
    application = Application()

    load_files("routes")

    application.run()
