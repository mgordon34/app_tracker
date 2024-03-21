from rest_framework import serializers

from app_tracker.application.models import Application, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "application", "text"]


class ApplicationSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

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
