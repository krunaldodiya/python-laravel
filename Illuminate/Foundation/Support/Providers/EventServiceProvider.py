from Illuminate.Support.ServiceProvider import ServiceProvider


class EventServiceProvider(ServiceProvider):
    def register(self):
        print("registering events")

    def boot(self):
        pass
