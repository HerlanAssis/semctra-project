from rest_framework import viewsets
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from apps.users.api.permissions import IsHealth_Professional, IsPatient, checkIfUserIsAHealthProfessional
from ..models import Meet, Queue
from ..enums import StatusEnum, StatusMeetEnum
from .serializers import MeetSerializer, QueueSerializer
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
            permission_classes = [IsHealth_Professional, ]
        else:
            permission_classes = [IsOwnerOrReject]
        return [permission() for permission in permission_classes]

    def create(self, request):
        # verifica se esta com alguma consulta ativa
        current_meet = Meet.objects.filter(
            Q(host=request.user) &
            Q(status=StatusMeetEnum.STARTED.value[0])
        ).first()

        # Encerra se existir
        if current_meet is not None:
            return Response(data={'detail': 'Você já tem uma consulta ativa'}, status=status.HTTP_409_CONFLICT)

        # Recuperar o primeiro da fila
        patient_queued = Queue.objects.filter(
            Q(status=StatusEnum.PROCESSING.value[0])).first()

        if patient_queued is not None:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(
                host=request.user, requester=patient_queued.requester)

            data = serializer.data
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(data={'detail': 'Nenhum paciente na fila'}, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False, permission_classes=[IsHealth_Professional, ])
    def finish(self, request):
        # Recupera a solicitação mais antiga
        meet = Meet.objects.filter(
            Q(status=StatusMeetEnum.STARTED.value[0]) &
            Q(host=request.user)
        ).first()

        if meet is not None:
            meet.status = StatusMeetEnum.CLOSED.value[0]
            meet.save()
            return Response(data={'detail': 'Consulta encerrada!'}, status=status.HTTP_200_OK)
        return Response(data={'detail': 'Nenhuma consulta pendente'}, status=status.HTTP_200_OK)


class QueueViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows member to be viewed or edited.
    """
    serializer_class = QueueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if checkIfUserIsAHealthProfessional(user):
            return Queue.objects.filter(Q(status=StatusEnum.PROCESSING.value[0]))

        return Queue.objects.filter(Q(requester=user))

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsPatient, IsUpdaterOrReject, ]
        elif self.action == 'create':
            permission_classes = [IsPatient, ]
        else:
            permission_classes = [IsOwnerOrReject]
        return [permission() for permission in permission_classes]

    def create(self, request):
        already_queued = Queue.objects.filter(Q(requester=request.user) & Q(
            status=StatusEnum.PROCESSING.value[0]))

        if already_queued.count() > 0:
            return Response(data={'detail': 'Já existe uma solicitação pendente!'}, status=status.HTTP_409_CONFLICT)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(requester=request.user)
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)
