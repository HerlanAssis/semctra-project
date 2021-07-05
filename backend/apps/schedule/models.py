from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from .enums import DaysEnum


User = get_user_model()


class Event(models.Model):
    owner = models.ForeignKey(
        to=User,
        verbose_name=_('Dono'),
        on_delete=models.CASCADE,
        related_name='eventos',
    )
    week_day = models.CharField(
        choices=DaysEnum.choices(),
        max_length=32,
        default=DaysEnum.MONDAY.value[0]
    )
    start_time = models.TimeField(
        verbose_name=_('Hora de início')
    )
    end_time = models.TimeField(
        verbose_name=_('Hora de fim')
    )

    class Meta:
        verbose_name = _("Evento")
        verbose_name_plural = _("Eventos")

    def __str__(self):
        return "{} - Início: {} | Fim: {}".format(self.week_day, self.start_time, self.end_time)
