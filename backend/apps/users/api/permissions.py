from rest_framework import permissions
from ..enum import RolesEnum


class IsOwnerOrReject(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        return obj == request.user


class IsHealth_Professional(permissions.BasePermission):
    def has_permission(self, request, view):
        return checkIfUserIsAHealthProfessional(health_professional=request.user)


class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return checkIfUserIsAPatient(patient=request.user)


def checkIfUserIsAPatient(patient):
    user_roles = [role.id for role in patient.roles.all()]
    return RolesEnum.PATIENT.value[0] in user_roles


def checkIfUserIsAHealthProfessional(health_professional):
    user_roles = [role.id for role in health_professional.roles.all()]
    return RolesEnum.HEALTH_PROFESSIONAL[0].value in user_roles
