from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.roles.api.views import RoleViewSet, UserRoleViewSet

router = DefaultRouter()
router.register(r"roles", RoleViewSet, basename="role")
router.register(r"user-roles", UserRoleViewSet, basename="user-role")

urlpatterns = [
    path("", include(router.urls)),
]
