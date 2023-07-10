from core.application import router

router.get("/", ["HomeController", "home"])

router.get("/test", ["HomeController", "create"])
router.post("/test", ["HomeController", "store"])

router.get("/users/:username", ["HomeController", "user"])
router.get("/closure", lambda request: "testing")
