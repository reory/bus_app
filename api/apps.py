# Base class for configuring Django applications.
from django.apps import AppConfig


class ApiConfig(AppConfig):

    # Sets the default type for automatically created primary keys.
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
