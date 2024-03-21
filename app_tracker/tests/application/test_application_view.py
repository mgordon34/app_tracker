import pytest

from app_tracker.application.models import Application
from app_tracker.tests.utils import create_user


@pytest.mark.django_db
def test_create_application(client):
    user = create_user(["AppCreator"])
    client.force_authenticate(user=user)

    applicant_name = "Test Applicant"

    payload = {"applicant_name": applicant_name}
    response = client.post("/applications/", payload)
    assert response.status_code == 201
    application = Application.objects.first()
    assert application is not None
    assert application.applicant_name == applicant_name
