from django.db.models.signals import post_save
from django.db.models import Q
from django.dispatch import receiver
from .models import Meet, Queue
from .enums import StatusMeetEnum, StatusEnum


@receiver(post_save, sender=Meet)
def create_meet(sender, instance, created, **kwargs):

    if created:
        patient_queued = Queue.objects.filter(
            Q(status=StatusEnum.PROCESSING.value[0]) &
            Q(requester=instance.requester)
        ).first()

        patient_queued.status = StatusEnum.ACCEPTED.value[0]
        patient_queued.save()
        instance.save()
    else:
        if instance.status == StatusMeetEnum.CLOSED.value[0]:
            patient_queued = Queue.objects.filter(
                Q(status=StatusEnum.ACCEPTED.value[0]) &
                Q(requester=instance.requester)
            ).first()
            print(patient_queued)

            patient_queued.status = StatusEnum.FINISHED.value[0]
            patient_queued.save()
