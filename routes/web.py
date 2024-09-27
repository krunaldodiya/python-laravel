import builtins

from Illuminate.Http.Request import Request
from Illuminate.Support.Facades.App import App
from Illuminate.Support.Facades.Redirect import Redirect
from app.Http.Controllers.HomeController import HomeController
from Illuminate.Support.Facades.Route import Route


def home(request: Request):
    router = App.make("app")

    print("test")

    builtins.dd(router)


def test(request: Request):
    return Redirect.to("/home")


def hello(request: Request):
    return "test"


Route.get("/", home)
Route.get("/test", test)
Route.get("/api/hello", hello)

Route.get("/home", [HomeController, "home"])
Route.get("/users", [HomeController, "create"])
Route.post("/users", [HomeController, "store"])
Route.get("/users/:username", [HomeController, "user"])
