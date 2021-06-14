from django.db import models
from django.utils.translation import ugettext_lazy as _

from .enums import DaysEnum

# Create your models here.
class Schedule(models.Model):
    description = models.CharField(_('Descrição'), max_length=128)
    
    class Meta:
        verbose_name = _("Agenda")
        verbose_name_plural = _("Agendas")

    def __str__(self):
        return "{}".format(self.description)
    

class Event(models.Model):
    schedule = models.ForeignKey(
        to=Schedule,
        verbose_name=_('Agenda'),
        on_delete=models.CASCADE,
        related_name='eventos',
    )

    week_day = models.CharField(
        choices=DaysEnum.choices(),
        max_length=32,
        default=DaysEnum.MONDAY.value[0]
    )

    class Meta:
        verbose_name = _("Evento")
        verbose_name_plural = _("Eventos")

    def __str__(self):
        return "{} - {}".format(self.schedule, self.week_day)
    

class Interval(models.Model):    
    event = models.ForeignKey(
        to=Event,
        verbose_name=_('Evento'),
        on_delete=models.CASCADE,
        related_name='intervalos',
    )

    start_time = models.DateTimeField(
        verbose_name=_('Data e hora de início')
    )
    end_time = models.DateTimeField(
        verbose_name=_('Data e hora de fim')
    )

    class Meta:
        verbose_name = _("Intervalo")
        verbose_name_plural = _("Intervalos")

    def __str__(self):
        return "Início: {} | Fim: {}".format(self.start_time, self.end_time)