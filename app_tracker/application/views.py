from rest_framework import viewsets

from app_tracker.application.permissions import HasGroupPermission
from app_tracker.application.serializers import (
    ApplicationSerializer,
    CommentSerializer,
)
from app_tracker.application.models import Application, Comment


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [HasGroupPermission]
    permission_groups = {
        "list": ["AppViewer"],
        "create": ["AppCreator"],
        "update": ["AppApprover"],
        "partial_update": ["AppApprover"],
        "retrieve": ["AppViewer"],
        "destory": ["AppEditor"],
    }
    queryset = Application.objects.all()

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        fields = [
            "id",
            "applicant_name",
            "status",
            "created",
            "modified",
        ]

        if self.action in [
            "list",
            "create",
            "update",
            "partial_update",
            "destroy",
        ]:
            kwargs["fields"] = fields
        elif self.action == "retrieve":
            fields.append("comments")
            kwargs["fields"] = fields

        return self.serializer_class(*args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()

    serializer_class = CommentSerializer
