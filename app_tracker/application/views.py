from rest_framework import viewsets

from app_tracker.application.serializers import (
    ApplicationSerializer,
    CommentSerializer,
)
from app_tracker.application.models import Application, Comment


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()

    serializer_class = ApplicationSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()

    serializer_class = CommentSerializer
