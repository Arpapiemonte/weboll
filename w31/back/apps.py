from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = "w31.back"
    label = "w31_back"

    def ready(self):
        import w31.back.signals  # noqa
