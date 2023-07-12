from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TurbineDataConfig(AppConfig):
    name = "turbine.turbine_data"
    verbose_name = _("Turbine Data")

    def ready(self):
        try:
            import turbine.turbine_data.signals  # noqa: F401
        except ImportError:
            pass
