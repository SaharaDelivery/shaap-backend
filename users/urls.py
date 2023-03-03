from django.urls import path

from users.apis import (
    DisableUserAccountApi,
    EditUserAccountApi,
    GetUserAccountApi,
    LoginApi,
    LogoutApi,
    RegisterUserApi,
)
from users.order_apis import PlaceOrderApi

urlpatterns = [
    path("register/", RegisterUserApi.as_view(), name="signup"),
    path("get-account/", GetUserAccountApi.as_view(), name="get-profile"),
    path("edit-account/", EditUserAccountApi.as_view(), name="edit-profile"),
    path("disable-account/", DisableUserAccountApi.as_view(), name="disable-account"),
    #########
    #########
    # path("verify-email/", VerifyEmailApi.as_view(), name="verify-email"),
    # path("forgot-password/", ForgotPasswordApi.as_view(), name="forgot-password"),
    # path("change-password/", ChangePasswordApi.as_view(), name="change-password"),
    #######
    #######
    path("place-order/", PlaceOrderApi.as_view(), name="place-order"),
    # path("edit-order/", EditOrderApi.as_view(), name="edit-order"),
    # path("add-to-order/", AddToOrderApi.as_view(), name="add-to-cart"),
    # path("edit-order-item/", EditOrderItemApi.as_view(), name="edit-cart-item"),
    # path("remove-from-order/", RemoveFromOrderApi.as_view(), name="remove-from-cart"),
    # path("get-order-details/", GetOrderDetailsApi.as_view(), name="get-cart"),
    # path("get-all-pending-orders/", GetAllPendingOrdersApi.as_view(), name="get-all-pending-orders"),
    # path("get-all-completed-orders/", GetAllCompletedOrdersApi.as_view(), name="get-all-completed-orders"),
    # path("get-saved-orders/", GetSavedOrdersApi.as_view(), name="get-saved-orders"),
    # path("get-order-history/", GetOrderHistoryApi.as_view(), name="get-order-history"),
    #######
    #######
    # path("add-address/", AddAddressApi.as_view(), name="add-address"),
    # path("get-saved-addresses/", GetSavedAddressesApi.as_view(), name="get-saved-addresses"),
    # path("edit-address/", EditAddressApi.as_view(), name="edit-address"),
    #######
    #######
    path("login/", LoginApi.as_view(), name="login"),
    path("logout/", LogoutApi.as_view(), name="logout"),
]
