from django.apps import AppConfig
from django.core.management import call_command

from delivery.configs.settings import ENVIRONMENT


class DeliveryConfig(AppConfig):
    name = "delivery"
    verbose_name = "delivery application"

    def ready(self):
        if ENVIRONMENT == "prod":
            call_command("migrate")
