import json

from core.Support.Facades.View import View
from core.controller import Controller
from core.helpers import *


class HomeController(Controller):
    def home(self, request):
        return View.make("home")

    def create(self, request):
        return View.make("index", {"name": "krunal"})

    def store(self, request):
        return json.dumps(request.body)

    def user(self, request):
        username = request.get("username")

        return f"hello, {username}"
