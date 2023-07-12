import json

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

    def home(self, request):
        return View.make("home")

    def create(self, request):
        return View.make("index", {"name": "krunal"})

    def store(self, request):
        return json.dumps(request.body)

    def user(self, request):
        username = request.get("username")

        return {"username": username, "name": self.service.another_service.get_name()}
