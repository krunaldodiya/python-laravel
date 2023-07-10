from core.application import router

from core.helpers import *

router.get("/", ["HomeController", "home"])

router.get("/test", ["HomeController", "create"])
router.post("/test", ["HomeController", "store"])

router.get("/users/:username", ["HomeController", "user"])
router.get("/closure", lambda request: "testing")
