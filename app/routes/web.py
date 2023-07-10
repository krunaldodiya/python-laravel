from core.application import router

router.get("/", ["HomeController", "home"])
router.get("/test", ["HomeController", "test"])
router.get("/users/:username", ["HomeController", "user"])
router.get("/closure", lambda request: "testing")
