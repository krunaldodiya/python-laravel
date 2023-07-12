import json

from Illuminate.Support.Facades.View import View
from Illuminate.controller import Controller
from Illuminate.helpers import *


class HomeController(Controller):
    def home(self, request):
        return View.make("home")

    def create(self, request):
        return View.make("index", {"name": "krunal"})

    def store(self, request):
        return json.dumps(request.body)

    def user(self, request):
        username = request.get("username")

        return {"username": username}
