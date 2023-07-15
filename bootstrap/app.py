from pathlib import Path

from Illuminate.Contracts.Http.Kernel import Kernel

from app.Http.Kernel import Kernel as HttpKernel

from Illuminate.Foundation.Application import Application

path = Path()

application = Application(path.cwd())

application.singleton(Kernel, HttpKernel)
