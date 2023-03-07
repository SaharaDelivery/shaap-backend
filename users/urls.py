from django.urls import path

from users.apis import (
    DisableUserAccountApi,
    EditUserAccountApi,
    GetUserAccountApi,
    LoginApi,
    LogoutApi,
    RegisterUserApi,
    SetupUserAccountApi,
)
from users.order_apis import (
    AddOrderAddressApi,
    AddOrderItemApi,
    DeleteOrderItem,
    EditOrderAddressApi,
    GetAllOrderItemsApi,
    GetOrderBasedOnStatus,
    GetOrderDetailsApi,
    GetOrderHistoryApi,
    GetSavedUserOrderAddressApi,
    PlaceOrderApi,
    ReduceOrderItemQuantityApi,
)

urlpatterns = [
    path("account/register/", RegisterUserApi.as_view(), name="signup"),
    path("account/setup/<int:user_id>/", SetupUserAccountApi.as_view(), name="set-profile"),
    path("account/get/", GetUserAccountApi.as_view(), name="get-profile"),
    path("account/edit/", EditUserAccountApi.as_view(), name="edit-profile"),
    #########
    #########
    # path("verify-email/", VerifyEmailApi.as_view(), name="verify-email"),
    # path("forgot-password/", ForgotPasswordApi.as_view(), name="forgot-password"),
    # path("change-password/", ChangePasswordApi.as_view(), name="change-password"),
    # path("change-email/", ChangeEmailApi.as_view(), name="change-email"),
    # path("change-username/", ChangeUsernameApi.as_view(), name="change-username"),
    # path("account/disable", DisableUserAccountApi.as_view(), name="disable-account"),
    #######
    #######
    path("order/place/", PlaceOrderApi.as_view(), name="place-order"),
    path(
        "orders/get/<str:order_status>/",
        GetOrderBasedOnStatus.as_view(),
        name="get-orders-based-on-status",
    ),
    path("order/details/", GetOrderDetailsApi.as_view(), name="get-cart"),
    path("order/history/", GetOrderHistoryApi.as_view(), name="get-order-history"),
    ####
    ####
    path("order/address/add/", AddOrderAddressApi.as_view(), name="add-order-address"),
    path(
        "order/address/get/saved/",
        GetSavedUserOrderAddressApi.as_view(),
        name="get-order-address",
    ),
    path(
        "order/address/edit/<int:address_id>/",
        EditOrderAddressApi.as_view(),
        name="edit-order-address",
    ),
    ####
    ####
    path(
        "order/item/get/all/<int:order_id>/",
        GetAllOrderItemsApi.as_view(),
        name="get-all-order-item",
    ),
    path("order/item/add/", AddOrderItemApi.as_view(), name="add-order-item"),
    path(
        "order/item/reduce/<int:order_item_id>/",
        ReduceOrderItemQuantityApi.as_view(),
        name="reduce-order-item-quantity",
    ),
    path(
        "order/item/delete/<int:order_item_id>/",
        DeleteOrderItem.as_view(),
        name="delete-order-item",
    ),
    #######
    #######
    path("login/", LoginApi.as_view(), name="login"),
    path("logout/", LogoutApi.as_view(), name="logout"),
]
