# users/utils.py

from django.contrib.auth import authenticate
from rest_framework import serializers
from apps.core.utils import get_unique_or_none
from django.contrib.auth import get_user_model

User = get_user_model()


def get_and_authenticate_user(username, password):
    # login using username or email
    user = get_unique_or_none(User, email=username) or get_unique_or_none(
        User, username=username)

    if user is None or authenticate(username=user.username, password=password) is None:
        raise serializers.ValidationError("Usuário ou senha inválidos!")
    return user
