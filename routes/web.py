from app.Http.Controllers.HomeController import HomeController
from Illuminate.Support.Facades.Route import Route

Route.get("/test/:id", lambda request: "testing")
Route.get("/test/test", [HomeController, "test"])
Route.get("/", [HomeController, "home"])
Route.get("/test", [HomeController, "create"])
Route.post("/test", [HomeController, "store"])
Route.get("/users/:username", [HomeController, "user"])
