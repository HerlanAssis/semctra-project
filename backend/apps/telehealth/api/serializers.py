from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField
from django.contrib.auth import get_user_model
import os
import jwt
from ..models import Meet
from ..enums import StatusEnum


User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class MeetSerializer(ModelSerializer):
    requester = UserSerializer(required=False, many=False)
    host = UserSerializer(required=False, many=False)
    token = SerializerMethodField()
    status = CharField(required=False, source='get_status_display')

    class Meta:
        model = Meet
        fields = (
            'id', 'requester', 'host',
            'token', 'link', 'pin',
            'status'
        )

    def get_token(self, obj):
        app_issue = os.environ.get("JITSI_APP_ISSUE", "smash")
        app_secret = os.environ.get("JITSI_APP_SECRET", "appjitsi")
        sub = os.environ.get("JITSI_DOMAIN", "jitsi.rsnascimento.info")

        context = self.context.get('request')
        user = context.user

        payload = {
            "context": {
                "user": {
                    "name": user.username,
                    "email": user.email
                }
            },
            "aud": app_issue,
            "iss": app_issue,
            "room": obj.pin,
            "sub": sub
        }

        return jwt.encode(payload, app_secret)
