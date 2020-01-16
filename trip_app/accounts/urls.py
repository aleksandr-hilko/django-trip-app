from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path("create/", views.UserCreate.as_view(), name="create"),
    path("", views.UserList.as_view(), name="users"),
    path("<int:pk>/", views.UserDetail.as_view(), name="user"),
    path("current/", views.CurrentUserAPIView.as_view(), name="current_user"),
]
