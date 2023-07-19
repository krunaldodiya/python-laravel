from Illuminate.Support.Facades.Facade import Facade


class Redirect(metaclass=Facade):
    @staticmethod
    def get_facade_accessor():
        return "redirect"
