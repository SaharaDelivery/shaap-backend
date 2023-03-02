from django.urls import path

from restaurants.apis import (
    ArchiveRestaurantApi,
    EditRestaurantInfoApi,
    GetAllFilteredRestaurantsApi,
    GetAllRestaurantsApi,
    GetRestaurantInfoApi,
    RegisterRestaurantApi,
    RestaurantStaffLoginApi,
    RestaurantStaffLogoutApi,
)

urlpatterns = [
    path("register/", RegisterRestaurantApi.as_view(), name="register-restaurant"),
    path("get/<int:id>/", GetRestaurantInfoApi.as_view(), name="get-restaurant-info"),
    path("get/all/", GetAllRestaurantsApi.as_view(), name="get-all-restaurants"),
    # path(
    #     "get/filter/",
    #     GetAllFilteredRestaurantsApi.as_view(),
    #     name="get-all-filtered-restaurants",
    # ),
    path(
        "edit/<int:id>/", EditRestaurantInfoApi.as_view(), name="edit-restaurant-info"
    ),
    path(
        "disable/<int:id>/", ArchiveRestaurantApi.as_view(), name="disable-restaurant"
    ),
    # ####
    # ####
    path(
        "staff/login/", RestaurantStaffLoginApi.as_view(), name="restaurant-staff-login"
    ),
    path(
        "staff/logout/",
        RestaurantStaffLogoutApi.as_view(),
        name="restaurant-staff-logout",
    ),
    # path("pending/orders/", GetPendingOrdersApi.as_view(), name="get-pending-orders"),
    # path("pending/orders/accept/", AcceptPendingOrderApi.as_view(), name="accept-pending-order"),
    # path("update/order/status/", UpdateOrderStatusApi.as_view(), name="update-order-status"),
    # path("completed/orders/", GetCompletedOrdersApi.as_view(), name="get-completed-orders"),
    # path("orders/all/", GetAllRestaurantOrdersApi.as_view(), name="get-all-orders"),
    # path("profile/views/", GetRestaurantProfileViewsApi.as_view(), name="get-restaurant-profile-views"),
    # path("revenue/", GetRestaurantRevenueApi.as_view(), name="get-restaurant-revenue"),
    # path("revenue/withdraw/", WithdrawRestaurantRevenueApi.as_view(), name="withdraw-restaurant-revenue"),
    # ####
    # ####
    # path("create/menu/", CreateRestaurantMenuApi.as_view(), name="create-restaurant-menu"),
    # path("get/menu/", GetRestaurantMenuApi.as_view(), name="get-restaurant-menu"),
    # path("get/menu/all/", GetAllRestaurantMenusApi.as_view(), name="get-all-restaurant-menus"),
    # path("menu/edit/", EditRestaurantMenuApi.as_view(), name="edit-restaurant-menu"),
    # path("menu/archive/", ArchiveRestaurantMenuApi.as_view(), name="archive-restaurant-menu"),
    # path("menu/delete/", DeleteRestaurantMenuApi.as_view(), name="delete-restaurant-menu"),
    # ####
    # ####
    # path("create/menu/item/", CreateRestaurantMenuItemApi.as_view(), name="create-restaurant-menu-item"),
    # path("get/menu/item/", GetRestaurantMenuItemInfo.as_view(), name="get-restaurant-menu-item-info"),
    # path("get/menu/items/all/", GetAllRestaurantMenuItemsApi.as_view(), name="get-restaurant-menu-items"),
    # path("menu/item/edit/", EditRestaurantMenuItem.as_view(), name="edit-restaurant-menu-item"),
    # path("menu/item/archive/", ArchiveRestaurantMenuItemApi.as_view(), name="archive-restaurant-menu-item"),
    # path("menu/item/delete/", DeleteRestaurantMenuItemApi.as_view(), name="delete-restaurant-menu-item"),
    ####
    ####
]
