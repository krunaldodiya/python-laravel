import os

from Illuminate.View.ViewServiceProvider import ViewServiceProvider

from app.Providers.AppServiceProvider import AppServiceProvider
from app.Providers.EventServiceProvider import EventServiceProvider
from app.Providers.RouteServiceProvider import RouteServiceProvider


app = {
    "name": os.getenv("APP_NAME", "Flight"),
    "env": os.getenv("APP_ENV", "production"),
    "url": os.getenv("APP_URL", "http://localhost"),
    "asset_url": os.getenv("ASSET_URL"),
    "timezone": "Asia/Kolkata",
    "key": os.getenv("APP_KEY"),
    "providers": [
        ViewServiceProvider,
        AppServiceProvider,
        EventServiceProvider,
        RouteServiceProvider,
    ],
}
