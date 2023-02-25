from django.urls import path

from users.views import SignUpApi

urlpatterns = [
    path("signup/", SignUpApi.as_view(), name="signup")
]