import json

from Illuminate.Http.RequestAdapter import RequestAdapter
from Illuminate.Http.ServerBag.WSGIServer import WSGIServer


class WSGIRequestAdapter(RequestAdapter):
    def __init__(self, request: WSGIServer):
        self.request: WSGIServer = request

    def get_url(self):
        return self.request.path

    def get_full_url(self):
        return self.request.get_full_path()

    def query_data(self):
        return self.request.GET.dict()

    def post_data(self):
        try:
            return json.loads(self.request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return {}
