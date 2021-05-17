from django.utils.translation import ugettext_lazy as _
from enum import Enum


class StatusEnum(Enum):
    PROCESSING = ('PROCESSING', _('Em processamento'))
    ACCEPTED = ('ACCEPTED', _('Aceito'))
    FINISHED = ('FINISHED', _('Finalizado'))
    CANCELED = ('CANCELED', _('Cancelado'))

    @classmethod
    def choices(cls):
        return tuple((i.value[0], i.value[1]) for i in cls)
