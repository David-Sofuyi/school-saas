from rest_framework import viewsets, permissions
from apps.accounts.models import CustomUser
from apps.accounts.serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserMinimalSerializer,
)
from apps.core.mixins import TenantQuerySetMixin
from apps.core.permissions import HasSchoolAccess, IsSchoolStaff


class UserViewSet(TenantQuerySetMixin, viewsets.ModelViewSet):
    """
    API endpoint for managing users within the active tenant school.
    Lists, retrieves, creates, and updates school users.
    """
    queryset = CustomUser.objects.all().select_related("school")
    permission_classes = [permissions.IsAuthenticated, HasSchoolAccess]

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        if self.action == "list":
            return UserMinimalSerializer
        return UserSerializer

    def perform_create(self, serializer):
        # Automatically assign school context from request if not explicitly provided
        school = getattr(self.request, "school", None)
        if school and "school" not in serializer.validated_data:
            serializer.save(school=school)
        else:
            serializer.save()
