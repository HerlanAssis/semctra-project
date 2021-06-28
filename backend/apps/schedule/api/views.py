from rest_framework import viewsets
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from apps.users.api.permissions import IsHealth_Professional
from ..models import Event
from ..enums import DaysEnum
from .serializers import EventSerializer
from .permissions import IsOwnerOrReject, IsUpdaterOrReject


class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows member to be viewed or edited.
    """
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Event.objects.filter(Q(owner=user))

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsHealth_Professional, IsUpdaterOrReject, ]
        elif self.action == 'create':
            permission_classes = [IsHealth_Professional, ]
        else:
            permission_classes = [IsOwnerOrReject]
        return [permission() for permission in permission_classes]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(methods=['GET', ], detail=False, permission_classes=[IsHealth_Professional, ], url_path='week-day-options')
    def week_days_options(self, request):
        data = dict((x, y) for x, y in DaysEnum.choices())
        return Response(data, status=status.HTTP_200_OK)
