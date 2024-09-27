import json

from Illuminate.Http.Request import Request

from Illuminate.Support.Facades.View import View
from Illuminate.controller import Controller
from Illuminate.helpers import *


class AnotherService:
    def get_name(self):
        return "AnotherService"


class Service:
    def __init__(self, another_service: AnotherService) -> None:
        self.another_service = another_service

    def get_name(self):
        return "Service"


class Database:
    def __init__(self, another_service: AnotherService) -> None:
        self.another_service = another_service

    def get_name(self):
        return "Database"


class HomeController(Controller):

    def __init__(self, service: Service, database: Database) -> None:
        self.service = service

        self.middleware = []

    def home(self, request: Request):
        return View.make("home")

    def create(self, request: Request):
        return View.make("index", {"name": "krunal"})

    def store(self, request: Request):
        return json.dumps(request.body)

    def user(self, request: Request):
        username = request.get("username")

        return {"username": username, "name": self.service.another_service.get_name()}
