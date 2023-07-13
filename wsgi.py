from Illuminate.Support.Foundation.Application import Application
from Illuminate.file_loader import load_files

application = Application()

if __name__ == "__main__":
    load_files("routes")
    application.run()
