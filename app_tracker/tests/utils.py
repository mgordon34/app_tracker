from typing import List

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User
from model_bakery import baker


def create_user(groups: List[str]) -> User:
    user = baker.make(
        get_user_model(),
    )
    [user.groups.add(Group.objects.get(name=group)) for group in groups]

    return user
