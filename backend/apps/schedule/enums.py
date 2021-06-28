from django.utils.translation import ugettext_lazy as _
from enum import Enum


class DaysEnum(Enum):
    SUNDAY = ('SUNDAY', _('Domingo'))
    MONDAY = ('MONDAY', _('Segunda-Feira'))
    TUESDAY = ('TUESDAY', _('Terça-Feira'))
    WEDNESDAY = ('WEDNESDAY', _('Quarta-Feira'))
    THURSDAY = ('THURSDAY', _('Quinta-Feira'))
    FRIDAY = ('FRIDAY', _('Sexta-Feira'))
    SATURDAY = ('SATURDAY', _('Sábado'))

    @classmethod
    def choices(cls):
        return tuple((i.value[0], i.value[1]) for i in cls)
