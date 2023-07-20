from app.Http.Controllers.HomeController import HomeController
from Illuminate.Support.Facades.Route import Route

Route.get("/", lambda request: "testing")
Route.get("/users/home", [HomeController, "home"])
Route.get("/users", [HomeController, "create"])
Route.post("/users", [HomeController, "store"])
Route.get("/users/:username", [HomeController, "user"])
Route.get("/krunal", lambda request: "hello krunal")
