from rest_framework import viewsets
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from apps.users.api.permissions import IsHealth_Professional, IsPatient
from ..models import Meet
from .serializers import MeetSerializer
from .permissions import IsOwnerOrReject, IsUpdaterOrReject


class MeetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows member to be viewed or edited.
    """
    serializer_class = MeetSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        return Meet.objects.filter(Q(host=user) | Q(requester=user))

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsHealth_Professional, IsUpdaterOrReject, ]
        elif self.action == 'create':
            permission_classes = [IsPatient, ]
        else:
            permission_classes = [IsOwnerOrReject]
        return [permission() for permission in permission_classes]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(requester=request.user)
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(methods=['POST', ], detail=False, permission_classes=[IsHealth_Professional, ])
    def accept(self, request):
        # Recupera a solicitação mais antiga
        meet = Meet.objects.filter(
            host__isnull=True).order_by('created_at').first()
        if meet is not None:
            serializer = self.get_serializer(
                meet, data=request.data, partial=True, many=False)
            serializer.is_valid(raise_exception=True)
            serializer.save(host=request.user)
            return Response(serializer.data)
        return Response(data={'detail': 'Nenhuma consulta pendente'}, status=status.HTTP_200_OK)
