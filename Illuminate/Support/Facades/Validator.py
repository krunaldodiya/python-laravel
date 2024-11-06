from Illuminate.Support.Facades.Facade import Facade


class Validator(metaclass=Facade):
    @classmethod
    def get_facade_accessor(cls):
        return "validator"
