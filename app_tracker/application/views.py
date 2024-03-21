from rest_framework import viewsets

from app_tracker.application.serializers import ApplicationSerializer
from app_tracker.application.models import Application


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()

    serializer_class = ApplicationSerializer
