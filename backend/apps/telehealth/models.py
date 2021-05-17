from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint
from apps.core.models import BaseModel
from apps.telehealth.enums import StatusEnum
from apps.core.utils import create_hash


class Meet(BaseModel):
    requester = models.ForeignKey(
        to=get_user_model(),
        verbose_name=_('Solicitante'),
        on_delete=models.CASCADE,
        related_name='requested_meetings',
    )
    host = models.ForeignKey(
        to=get_user_model(),
        verbose_name=_('Anfitrião'),
        blank=True,
        null=True,
        related_name="hosted_meetings",
        on_delete=models.CASCADE
    )
    scheduled_to = models.DateTimeField(
        _("Agendado para"),
        blank=True,
        null=True,
    )
    link = models.URLField(
        _("Link"),
        blank=True,
        null=True,
    )
    status = models.CharField(
        choices=StatusEnum.choices(),
        max_length=32,
        default=StatusEnum.PROCESSING.value[0]
    )
    pin = models.CharField(
        _("Pin"),
        blank=True,
        null=True,
        max_length=32,
        default=create_hash,
        editable=False
    )

    class Meta:
        verbose_name = _("Meet")
        verbose_name_plural = _("Meet")
        constraints = [
            UniqueConstraint(fields=['pin'], name='unique pin'),
        ]

    def __str__(self):
        return "Agendado para: {}".format(self.scheduled_to)
