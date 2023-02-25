from django.urls import path

from users.views import LoginApi, SignUpApi

urlpatterns = [
    path("signup/", SignUpApi.as_view(), name="signup"),
    path("login/", LoginApi.as_view(), name="login"),
]
