from core.Support.Facades.Route import Route

Route.get("/", ["HomeController", "home"])
Route.get("/test", ["HomeController", "create"])
Route.post("/test", ["HomeController", "store"])
Route.get("/users/:username", ["HomeController", "user"])
Route.get("/closure", lambda request: "testing")
