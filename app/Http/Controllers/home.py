from core.Support.Facades.View import View
from core.controller import Controller
from core.helpers import *
from core.template import Template


class HomeController(Controller):
    def __init__(self) -> None:
        self.template = Template()

    def home(self, request):
        return View.make("home")

    def create(self, request):
        return View.make("index", {"name": "krunal"})

    def store(self, request):
        return config("app")

    def user(self, request):
        username = request.get("username")

        return f"hello, {username}"
