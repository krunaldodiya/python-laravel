from core.controller import Controller


class HomeController(Controller):
    def home(self, request):
        return "home"

    def test(self, request):
        return "test"

    def user(self, request):
        username = request.get("username")

        return f"hello, {username}"
