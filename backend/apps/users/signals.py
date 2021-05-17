from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Role, PatientProfile, DoctorProfile
from .enum import RolesEnum


@receiver(post_save, sender=PatientProfile)
def create_patient_role(sender, instance, created, **kwargs):
    if created:
        role_name = RolesEnum.PATIENT.value[0]
        role, status = Role.objects.get_or_create(id=role_name)
        instance.user.roles.add(role)
        instance.save()


@receiver(post_save, sender=DoctorProfile)
def create_doctor_role(sender, instance, created, **kwargs):
    if created:
        role_name = RolesEnum.HEALTH_PROFESSIONAL.value[0]
        role, status = Role.objects.get_or_create(id=role_name)
        instance.user.roles.add(role)
        instance.save()
