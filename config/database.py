import os

database = {
    "name": os.getenv("APP_NAME", "Flight"),
    "env": os.getenv("APP_ENV", "production"),
    "url": os.getenv("APP_URL", "http://localhost"),
    "asset_url": os.getenv("ASSET_URL"),
    "timezone": "Asia/Kolkata",
    "key": os.getenv("APP_KEY"),
}
