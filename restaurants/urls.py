from django.urls import path

from restaurants.apis import (
    ArchiveRestaurantApi,
    ArchiveRestaurantMenuApi,
    CreateRestaurantMenuApi,
    DeleteRestaurantMenuApi,
    EditRestaurantInfoApi,
    EditRestaurantMenuApi,
    GetArchivedRestaurantMenusApi,
    GetAllFilteredRestaurantsApi,
    GetAllRestaurantMenusApi,
    GetAllRestaurantsApi,
    GetRestaurantInfoApi,
    GetRestaurantMenuDetailsApi,
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
    path(
        "staff/login/", RestaurantStaffLoginApi.as_view(), name="restaurant-staff-login"
    ),
    path(
        "staff/logout/",
        RestaurantStaffLogoutApi.as_view(),
        name="restaurant-staff-logout",
    ),
    # path("profile/views/", GetRestaurantProfileViewsApi.as_view(), name="get-restaurant-profile-views"),
    ####
    ####
    # path("order/pending/get/", GetPendingOrdersApi.as_view(), name="get-pending-orders"),
    # path("orders/pending/accept/", AcceptPendingOrderApi.as_view(), name="accept-pending-order"),
    # path("order/update/status/", UpdateOrderStatusApi.as_view(), name="update-order-status"),
    # path("completed/orders/", GetCompletedOrdersApi.as_view(), name="get-completed-orders"),
    # path("orders/all/", GetAllRestaurantOrdersApi.as_view(), name="get-all-orders"),
    ####
    ####
    # path("revenue/", GetRestaurantRevenueApi.as_view(), name="get-restaurant-revenue"),
    # path("revenue/withdraw/", WithdrawRestaurantRevenueApi.as_view(), name="withdraw-restaurant-revenue"),
    # ####
    # ####
    path(
        "menu/create/", CreateRestaurantMenuApi.as_view(), name="create-restaurant-menu"
    ),
    path(
        "menu/get/<int:menu_id>/",
        GetRestaurantMenuDetailsApi.as_view(),
        name="get-restaurant-menu-details",
    ),
    path(
        "menu/get/all/<int:restaurant_id>/",
        GetAllRestaurantMenusApi.as_view(),
        name="get-all-restaurant-menus",
    ),
    path(
        "menu/get/archived/",
        GetArchivedRestaurantMenusApi.as_view(),
        name="get-archived-restaurant-menus",
    ),
    path(
        "menu/edit/<int:menu_id>/",
        EditRestaurantMenuApi.as_view(),
        name="edit-restaurant-menu",
    ),
    path(
        "menu/archive/<int:menu_id>/",
        ArchiveRestaurantMenuApi.as_view(),
        name="archive-restaurant-menu",
    ),
    path(
        "menu/delete/<int:menu_id>/",
        DeleteRestaurantMenuApi.as_view(),
        name="delete-restaurant-menu",
    ),
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
