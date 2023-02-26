from django.urls import path

from users.views import GetProfileApi, LoginApi, LogoutApi, SignUpApi

urlpatterns = [
    path("signup/", SignUpApi.as_view(), name="signup"),
    path("get-profile/", GetProfileApi.as_view(), name="get-profile"),
    # path("edit-profile/", EditProfileApi.as_view(), name="edit-profile"),
    # path("delete-account/", DeleteAccountApi.as_view(), name="delete-account"),
    
    # path("verify-email/", VerifyEmailApi.as_view(), name="verify-email"),
    # path("forgot-password/", ForgotPasswordApi.as_view(), name="forgot-password"),
    # path("change-password/", ChangePasswordApi.as_view(), name="change-password"),
    
    # path("add-address/", AddAddressApi.as_view(), name="add-address"),
    # path("get-address/", GetAddressApi.as_view(), name="get-address"),
    # path("edit-address/", EditAddressApi.as_view(), name="edit-address"),
    # path("delete-address/", DeleteAddressApi.as_view(), name="delete-address"),
    
    path("login/", LoginApi.as_view(), name="login"),
    path("logout/", LogoutApi.as_view(), name="logout"),
]
