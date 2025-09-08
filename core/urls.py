from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    # Index Views
    path("", views.HomeView.as_view(), name="home"),
    path("contact", views.ContactView.as_view(), name="contact"),
    # Profile detail view
    path("profile/", views.UserProfileView.as_view(), name="profile"),
    # Profile update view
    path("profile/edit/", views.UserProfileUpdateView.as_view(), name="profile_edit"),
    # Profile delete view
    path(
        "profile/delete/", views.UserProfileDeleteView.as_view(), name="profile_delete"
    ),
]
