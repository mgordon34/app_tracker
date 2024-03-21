from django.db import models

from app_tracker.application.enums.application_status import ApplicationStatus


class Application(models.Model):
    """Model used for storing/tracking application"""

    applicant_name = models.CharField(
        max_length=50,
    )
    status = models.CharField(
        default=ApplicationStatus.SUBMITTED.value,
        max_length=50,
        choices=ApplicationStatus.choices(),
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    """Model used for storing comments on an application"""

    application = models.ForeignKey(
        Application,
        related_name="comments",
        on_delete=models.CASCADE,
    )
    text = models.CharField(
        max_length=200,
    )
