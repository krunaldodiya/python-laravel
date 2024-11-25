from Illuminate.Foundation.Application import Application


application = (
    Application.configure(base_path="")
    .with_routing()
    .with_middleware()
    .with_exceptions()
    .create()
)
