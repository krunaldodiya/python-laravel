from app.Http.Controllers.HomeController import HomeController
from core.Support.Facades.Route import Route

Route.get("/closure", lambda request: "testing")
Route.get("/", [HomeController, "home"])
Route.get("/test", [HomeController, "create"])
Route.post("/test", [HomeController, "store"])
Route.get("/users/:username", [HomeController, "user"])
