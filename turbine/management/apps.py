from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ManagementConfig(AppConfig):
    name = "turbine.management"
    verbose_name = _("Management")

    def ready(self):
        try:
            import turbine.management.signals  # noqa: F401
        except ImportError:
            pass
