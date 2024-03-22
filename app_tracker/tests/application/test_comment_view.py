import pytest
from model_bakery import baker

from app_tracker.application.models import Application, Comment
from app_tracker.tests.utils import create_user


def assert_comments_match(mock_comments, json_comments):
    """Loop through each comment, asserting each value matches"""
    fields_to_check = [
        "id",
        "text",
    ]
    for i in range(0, len(mock_comments)):
        for field in fields_to_check:
            assert getattr(mock_comments[i], field) == json_comments[i][field]
        assert (
            mock_comments[i].application.id == json_comments[i]["application"]
        )


@pytest.mark.django_db
class TestCommentView:
    def test_create_comment(self, client):
        user = create_user(["AppEditor"])
        client.force_authenticate(user=user)
        text = "Test Comment"

        application = baker.make(Application)

        # call api
        payload = {"application": application.id, "text": text}
        response = client.post("/comments/", payload)

        comment = Comment.objects.first()
        assert response.status_code == 201
        assert comment is not None

    def test_list_applications(self, client):
        user = create_user(["AppViewer"])
        client.force_authenticate(user=user)

        application = baker.make(Application)

        # generate mock application
        mock_comments = [
            baker.make(Comment, application=application, text="Test Comment"),
            baker.make(
                Comment, application=application, text="Test Comment 2"
            ),
        ]

        # call api
        response = client.get("/comments/")

        assert response.status_code == 200
        comments = response.json()
        assert comments is not None
        assert len(comments) == len(mock_comments)
        assert_comments_match(mock_comments, comments)

    def test_unauthorized_returns_401(self, client):
        # call api
        response = client.get("/comments/")

        assert response.status_code == 401
        assert response.json() == {
            "detail": "Authentication credentials were not provided."
        }

    def test_wrong_group_returns_403(self, client):
        user = create_user(["AppEditor"])
        client.force_authenticate(user=user)

        # call api
        response = client.get("/comments/")

        assert response.status_code == 403
        assert response.json() == {
            "detail": "You do not have permission to perform this action."
        }
