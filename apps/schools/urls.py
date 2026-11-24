from django.urls import path

from apps.schools import views

app_name = "schools"

urlpatterns = [
    path("", views.SchoolListView.as_view(), name="school-list"),
    path("create/", views.SchoolCreateView.as_view(), name="school-create"),
    path("<int:pk>/", views.SchoolDetailView.as_view(), name="school-detail"),
    path("<int:pk>/edit/", views.SchoolUpdateView.as_view(), name="school-update"),
    path(
        "<int:pk>/settings/",
        views.SchoolSettingsView.as_view(),
        name="school-settings",
    ),
]
