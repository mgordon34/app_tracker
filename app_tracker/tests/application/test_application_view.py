import pytest
from model_bakery import baker

from app_tracker.application.models import Application
from app_tracker.tests.utils import create_user


def assert_applications_match(mock_applications, json_applications):
    """Loop through each application, asserting each value matches"""
    fields_to_check = [
        "id",
        "applicant_name",
        "status",
    ]
    for i in range(0, len(mock_applications)):
        for field in fields_to_check:
            assert (
                getattr(mock_applications[i], field)
                == json_applications[i][field]
            )


@pytest.mark.django_db
class TestApplication:
    def test_create_application(self, client):
        user = create_user(["AppCreator"])
        client.force_authenticate(user=user)
        applicant_name = "Test Applicant"

        # call api
        payload = {"applicant_name": applicant_name}
        response = client.post("/applications/", payload)

        application = Application.objects.first()
        assert response.status_code == 201
        assert application is not None
        assert application.applicant_name == applicant_name

    def test_list_applications(self, client):
        user = create_user(["AppViewer"])
        client.force_authenticate(user=user)
        applicant_name = "Test Applicant"

        # generate mock application
        mock_applications = [
            baker.make(Application, applicant_name=applicant_name),
            baker.make(
                Application, applicant_name=applicant_name, status="SUBMITTED"
            ),
        ]

        # call api
        response = client.get("/applications/")

        assert response.status_code == 200
        applications = response.json()
        assert applications is not None
        assert len(applications) == len(mock_applications)
        assert_applications_match(mock_applications, applications)

    def test_get_application(self, client):
        user = create_user(["AppViewer"])
        client.force_authenticate(user=user)
        applicant_name = "Test Applicant"

        # generate mock application
        mock_application = (
            baker.make(Application, applicant_name=applicant_name),
        )

        # call api
        response = client.get(f"/applications/{mock_application[0].id}/")

        assert response.status_code == 200
        application = response.json()
        assert application is not None
        assert_applications_match(mock_application, [application])

    @pytest.mark.parametrize(
        "status,expected_code",
        [
            ("ACCEPTED", 200),
            ("REJECTED", 200),
            ("bad_status", 400),
        ],
    )
    def test_edit_application(self, client, status, expected_code):
        user = create_user(["AppApprover"])
        client.force_authenticate(user=user)
        applicant_name = "Test Applicant"

        # generate mock application
        mock_application = (
            baker.make(Application, applicant_name=applicant_name),
        )
        payload = {"status": status}

        # call api
        response = client.patch(
            f"/applications/{mock_application[0].id}/", payload
        )

        application_json = response.json()
        assert response.status_code == expected_code
        if expected_code == 200:
            assert application_json["status"] == status

    def test_delete_application(self, client):
        user = create_user(["AppEditor"])
        client.force_authenticate(user=user)
        applicant_name = "Test Applicant"

        # generate mock application
        mock_application = (
            baker.make(Application, applicant_name=applicant_name),
        )

        assert len(Application.objects.all()) == 1

        # call api
        response = client.delete(f"/applications/{mock_application[0].id}/")

        assert response.status_code == 204
        assert len(Application.objects.all()) == 0

    def test_unauthorized_returns_401(self, client):
        # call api
        response = client.get("/applications/")

        assert response.status_code == 401
        assert response.json() == {
            "detail": "Authentication credentials were not provided."
        }

    def test_wrong_group_returns_403(self, client):
        user = create_user(["AppEditor"])
        client.force_authenticate(user=user)

        # call api
        response = client.get("/applications/")

        assert response.status_code == 403
        assert response.json() == {
            "detail": "You do not have permission to perform this action."
        }
