from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TelehealthConfig(AppConfig):
    name = 'apps.telehealth'
    verbose_name = _('Telesaúde')

    def ready(self):
        from . import signals
