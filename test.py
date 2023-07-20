import requests

from Illuminate.Http.ServerBag.WSGIServer import WSGIServer


class App:
    def run(self):
        self.sever = WSGIServer.get_server()

        requests.get("https://google.com/test")

        print("running", self.sever.environ)

        return ["test".encode("utf-8")]


def main(environ, start_response):
    if environ.get("HTTP_REFERER") == None:
        try:
            WSGIServer.create_server(environ, start_response)

            app = App()

            return app.run()
        finally:
            print("done")
    else:
        return []
