from Illuminate.Support.ServiceProvider import ServiceProvider


class RouteServiceProvider(ServiceProvider):
    def register(self):
        print("registering routes")

    def boot(self):
        pass
