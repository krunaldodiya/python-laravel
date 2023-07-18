from pathlib import Path

from Illuminate.Contracts.Http.Kernel import Kernel

from Illuminate.Foundation.Application import Application

from app.Http.Kernel import Kernel as HttpKernel

app: Application = Application(Path().cwd())

app.singleton(Kernel, HttpKernel)
