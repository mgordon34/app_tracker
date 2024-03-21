from django.urls import include, path
from rest_framework import routers

from app_tracker.application.views import ApplicationViewSet, CommentViewSet

router = routers.DefaultRouter()

router.register("applications", ApplicationViewSet)
router.register("comments", CommentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]
