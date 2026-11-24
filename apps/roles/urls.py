from django.urls import path

from apps.roles import views

app_name = "roles"

urlpatterns = [
    path("", views.RoleListView.as_view(), name="role-list"),
    path("create/", views.RoleCreateView.as_view(), name="role-create"),
    path("assign/", views.UserRoleAssignView.as_view(), name="user-role-assign"),
]
