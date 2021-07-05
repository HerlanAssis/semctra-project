from django.utils import timezone
from django.db.models.signals import post_save
from django.db.models import Q
from django.dispatch import receiver
from .models import Meet, Queue
from .enums import StatusMeetEnum, StatusEnum


@receiver(post_save, sender=Meet)
def create_meet(sender, instance, created, **kwargs):

    if created:
        # SE um novo meet for criado
        # Então adicione o primeiro da fila para ele
        patient_queued = Queue.objects.filter(
            Q(status=StatusEnum.PROCESSING.value[0]) &
            Q(requester=instance.requester)
        ).first()

        patient_queued.status = StatusEnum.ACCEPTED.value[0]
        patient_queued.save()
        instance.save()
    else:
        # SE o meet for encerrado
        # Então atualize o status do item da fila
        if instance.status == StatusMeetEnum.CLOSED.value[0]:
            patient_queued = Queue.objects.filter(
                Q(status=StatusEnum.ACCEPTED.value[0]) &
                Q(requester=instance.requester)
            ).first()

            patient_queued.status = StatusEnum.FINISHED.value[0]
            patient_queued.save()


@receiver(post_save, sender=Queue)
def finish_queue(sender, instance, created, **kwargs):
    if not created and instance.closed_in is None:
        # SE a solicitação da fila for aceita
        # Então adicione o tempo de fechado
        if instance.status == StatusEnum.ACCEPTED.value[0]:
            instance.closed_in = timezone.datetime.now()
            instance.save()
