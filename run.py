from werkzeug import run_simple
from wsgi import app


def run():
    run_simple(
        hostname="127.0.0.1",
        port=3000,
        application=app,
        use_debugger=True,
        use_reloader=True,
    )


if __name__ == "__main__":
    run()
