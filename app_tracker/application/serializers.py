from rest_framework import serializers

from app_tracker.application.models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["id", "applicant_name", "created", "modified"]
