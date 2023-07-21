from Illuminate.Http.Request import Request
from Illuminate.Support.Facades.Redirect import Redirect
from app.Http.Controllers.HomeController import HomeController
from Illuminate.Support.Facades.Route import Route


def home(request: Request):
    return request.method


def test(request: Request):
    return Redirect.to("/home")


Route.get("/", home)
Route.get("/test", test)

Route.get("/home", [HomeController, "home"])
Route.get("/users", [HomeController, "create"])
Route.post("/users", [HomeController, "store"])
Route.get("/users/:username", [HomeController, "user"])
