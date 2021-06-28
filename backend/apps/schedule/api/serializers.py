from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ChoiceField
from django.contrib.auth import get_user_model
from ..models import Event
from ..enums import DaysEnum


User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class EventSerializer(ModelSerializer):
    owner = UserSerializer(required=False, many=False)
    week_day = ChoiceField(required=True, choices=DaysEnum.choices())

    class Meta:
        model = Event
        fields = (
            'id', 'owner', 'week_day',
            'start_time', 'end_time',
        )

    def validate(self, data):
        """
        Check start_time is before end_time.
        """
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if start_time > end_time:
            raise serializers.ValidationError(
                {'detail': 'O fim do intervalo não pode ser menor que o início'}
            )

        return data
