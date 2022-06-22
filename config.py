import os


class Config(object):
    SITENAME = "Private-Net.work"
    SERVICE_NAME = "Notes"
    PROD_DOMAIN = "private-net.work"
    LANGUAGES = {
        "en": "English",
        "ru": "Russian"
    }

    PROJECT = os.getcwd()
    DB = f"{PROJECT}/data/db/main.db"

    SUPPORT_EMAIL = f"support@{PROD_DOMAIN}"
    ERROR_EMAIL = f"errors@{PROD_DOMAIN}"

    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
    AUTH_COOKIE = os.getenv("AUTH_COOKIE")

    TG_LOGGER_TOKEN = os.getenv("TG_LOGGER_TOKEN")
    TG_ADMIN_ID = os.getenv("TG_ADMIN_ID")


class ProductionConfig(Config):
    DOMAIN = "https://private-net.work"


class DevelopmentConfig(Config):
    DOMAIN = "http://localhost:5000"
