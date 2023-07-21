from werkzeug import run_simple
from wsgi import app


def run():
    run_simple(app, hostname="127.0.0.1", port=3000)


if __name__ == "__main__":
    run()
