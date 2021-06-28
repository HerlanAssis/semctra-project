from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from ..core.models import BaseModel
from .enum import RolesEnum


class Role(models.Model):
    '''
    The Role entries are managed by the system,
    automatically created via a Django data migration.
    '''

    id = models.CharField(choices=RolesEnum.choices(),
                          max_length=32, primary_key=True)

    def __str__(self):
        return self.get_id_display()


class User(AbstractUser):
    cpf = models.CharField(_('CPF'), max_length=32, blank=True, null=True)
    birthdate = models.DateField(
        _('Data de Nascimento'), blank=True, null=True)
    phone = models.CharField(
        _('Telefone'), max_length=32, blank=True, null=True)
    roles = models.ManyToManyField(Role)


class BaseProfile(BaseModel):
    user = models.OneToOneField(
        User, verbose_name=_('Usuário'), on_delete=models.CASCADE)

    class Meta:
        abstract = True


class PatientProfile(BaseProfile):
    sus_number = models.CharField(_('Número do SUS'), max_length=128)

    class Meta:
        verbose_name = _('Paciente')
        verbose_name_plural = _('Pacientes')
        default_related_name = 'patient_profile'

    def __str__(self):
        return self.sus_number


class DoctorProfile(BaseProfile):
    crm = models.CharField(_('CRM'), max_length=128)

    class Meta:
        verbose_name = _('Médico')
        verbose_name_plural = _('Médicos')
        default_related_name = 'doctor_profile'

    def __str__(self):
        return self.crm
