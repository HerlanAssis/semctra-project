from django.utils.translation import ugettext_lazy as _
from enum import Enum


class RolesEnum(Enum):
    ADMIN = ('ADMIN', _('Administrador'))
    HEALTH_PROFESSIONAL = ('HEALTH_PROFESSIONAL', _('Profissional da saúde'))
    PATIENT = ('PATIENT', _('Paciente'))

    @classmethod
    def choices(cls):
        return tuple((i.value[0], i.value[1]) for i in cls)
