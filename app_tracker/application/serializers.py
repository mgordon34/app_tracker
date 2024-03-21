from rest_framework import serializers

from app_tracker.application.models import Application, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "application", "text"]


class ApplicationSerializer(serializers.ModelSerializer):
    """
    Application Serializer. Related field comments is included for an
    individual GET of an application
    """

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    comments = CommentSerializer(many=True)
    status = serializers.CharField(required=False)

    class Meta:
        model = Application
        fields = [
            "id",
            "applicant_name",
            "status",
            "comments",
            "created",
            "modified",
        ]
