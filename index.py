from core.application import Application

application = Application()

application.boot()

from routes.web import *

application.run()
