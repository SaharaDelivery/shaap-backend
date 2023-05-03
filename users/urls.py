from django.urls import path

from users.apis import (
    ConfirmTokenApi,
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
    GetExistingUserRestaurantOrderApi,
    GetOrderBasedOnStatus,
    GetOrderDetailsApi,
    GetOrderHistoryApi,
    GetSavedUserOrderAddressApi,
    PlaceOrderApi,
    ReduceOrderItemQuantityApi,
)

urlpatterns = [
    path("account/token/", ConfirmTokenApi.as_view(), name="confirm-token"),
    path("account/login/", LoginApi.as_view(), name="login"),
    path("account/logout/", LogoutApi.as_view(), name="logout"),
    path("account/register/", RegisterUserApi.as_view(), name="signup"),
    path(
        "account/setup/<int:user_id>/",
        SetupUserAccountApi.as_view(),
        name="setup-profile",
    ),
    path("account/get/", GetUserAccountApi.as_view(), name="get-profile"),
    path("account/edit/", EditUserAccountApi.as_view(), name="edit-profile"),
    #########
    #########
    # path("email/verify", VerifyEmailApi.as_view(), name="verify-email"),
    # path("email/change/", ChangeEmailApi.as_view(), name="change-email"),
    # path("account/password/reset/", ResetPasswordApi.as_view(), name="reset-password"),
    # path("account/password/change/", ChangePasswordApi.as_view(), name="change-password"),
    # path("account/username/change/", ChangeUsernameApi.as_view(), name="change-username"),
    # path("account/disable/", DisableUserAccountApi.as_view(), name="disable-account"),
    #######
    #######
    path("order/place/", PlaceOrderApi.as_view(), name="place-order"),
    path(
        "orders/get/<str:order_status>/",
        GetOrderBasedOnStatus.as_view(),
        name="get-orders-based-on-status",
    ),
    path(
        "order/exists/<int:restaurant_id>/",
        GetExistingUserRestaurantOrderApi.as_view(),
        name="get-existing-user-restaurant-order",
    ),
    path("order/details/", GetOrderDetailsApi.as_view(), name="get-order-details"),
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
    path("order/item/add/", AddOrderItemApi.as_view(), name="add-order-item"),
    path(
        "order/item/get/all/<str:order_id>/",
        GetAllOrderItemsApi.as_view(),
        name="get-all-order-item",
    ),
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
]
