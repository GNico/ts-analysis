from django.apps import AppConfig


class TsaProjectConfig(AppConfig):
    name = 'ts_project'

    def ready(self):
        from ts_project import signals