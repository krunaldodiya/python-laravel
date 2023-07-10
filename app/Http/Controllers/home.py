from core.controller import Controller
from core.view import View


class HomeController(Controller):
    def home(self, request):
        return View.make("home")

    def create(self, request):
        return View.make("index", {"name": "krunal"})

    def store(self, request):
        return "test"

    def user(self, request):
        username = request.get("username")

        return f"hello, {username}"
