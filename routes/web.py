from Illuminate.Http.Request import Request
from app.Http.Controllers.HomeController import HomeController
from Illuminate.Support.Facades.Route import Route


def greetings(request: Request):
    return request.method


def test(request: Request):
    return "welcome"


Route.get("/", greetings)
Route.get("/test", test)

Route.get("/home", [HomeController, "home"])
Route.get("/users", [HomeController, "create"])
Route.post("/users", [HomeController, "store"])
Route.get("/users/:username", [HomeController, "user"])
