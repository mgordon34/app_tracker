# Generated by Django 5.0.3 on 2024-03-21 05:49

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import migrations
from django.utils import timezone


def generate_user(apps, username, groups, is_staff=False, is_superuser=False):
    User = get_user_model()

    user = User()
    user.username = username
    user.set_password("password")
    user.is_superuser = is_superuser
    user.is_staff = is_staff
    user.last_login = timezone.now()
    user.save()
    [user.groups.add(Group.objects.get(name=group)) for group in groups]
    user.save()


def apply_migration(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.bulk_create(
        [
            Group(name="AppViewer"),
            Group(name="AppCreator"),
            Group(name="AppEditor"),
            Group(name="AppApprover"),
        ]
    )

    users = [
        (
            "admin",
            ["AppViewer", "AppCreator", "AppEditor", "AppApprover"],
            True,
            True,
        ),
        ("app_viewer", ["AppViewer"]),
        ("app_creator", ["AppCreator"]),
        ("app_editor", ["AppEditor"]),
        ("app_approver", ["AppApprover"]),
    ]
    [generate_user(apps, *user) for user in users]


def revert_migration(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(
        name__in=[
            "AppViewer",
            "AppCreator",
            "AppEditor",
            "AppApprover",
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("application", "0001_initial"),
    ]

    operations = [migrations.RunPython(apply_migration, revert_migration)]