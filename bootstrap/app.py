from Illuminate.Contracts.Http.Kernel import Kernel

from Illuminate.Foundation.Application import Application

from Illuminate.Support.Facades.App import App

from app.Http.Kernel import Kernel as HttpKernel

application: Application = App.instance()

application.singleton(Kernel, HttpKernel)
