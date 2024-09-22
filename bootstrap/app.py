from pathlib import Path

from Illuminate.Contracts.Http.Kernel import Kernel

from Illuminate.Foundation.Application import Application

from app.Http.Kernel import Kernel as HttpKernel

from Illuminate.Support.Facades.Log import Log

import builtins

builtins.dd = lambda data: Log.dd(data)

app: Application = Application(Path().cwd())

app.singleton(Kernel, HttpKernel)
