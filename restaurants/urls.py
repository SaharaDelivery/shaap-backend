from django.urls import path

from restaurants.apis import (
    ArchiveRestaurantApi,
    ArchiveRestaurantMenuApi,
    ArchiveRestaurantMenuItemApi,
    CreateRestaurantMenuApi,
    CreateRestaurantMenuItemApi,
    DeleteRestaurantMenuApi,
    DeleteRestaurantMenuItemApi,
    EditRestaurantInfoApi,
    EditRestaurantMenuApi,
    EditRestaurantMenuItem,
    GetAllRestaurantCuisinesApi,
    GetAllRestaurantMenuItemsApi,
    # GetAllRestaurantMenuItemsUnderMenuApi,
    GetArchivedRestaurantMenusApi,
    GetAllFilteredRestaurantsApi,
    GetAllRestaurantMenusApi,
    GetAllRestaurantsApi,
    GetRestaurantInfoApi,
    GetRestaurantMenuDetailsApi,
    GetRestaurantMenuItemInfo,
    GetRestaurantWithCuisineApi,
    RegisterRestaurantApi,
    RestaurantStaffLoginApi,
    RestaurantStaffLogoutApi,
)

urlpatterns = [
    path("register/", RegisterRestaurantApi.as_view(), name="register-restaurant"),
    path("get/<int:id>/", GetRestaurantInfoApi.as_view(), name="get-restaurant-info"),
    path("get/all/", GetAllRestaurantsApi.as_view(), name="get-all-restaurants"),
    path(
        "cuisines/get/all/",
        GetAllRestaurantCuisinesApi.as_view(),
        name="get-all-restaurant-cuisines",
    ),
    path(
        "get/cuisine/<str:cuisine>/",
        GetRestaurantWithCuisineApi.as_view(),
        name="get-restaurant-that-has-current-cuisine",
    ),
    path(
        "filter/",
        GetAllFilteredRestaurantsApi.as_view(),
        name="get-all-filtered-restaurants",
    ),
    path(
        "edit/<int:id>/", EditRestaurantInfoApi.as_view(), name="edit-restaurant-info"
    ),
    # path("profile/views/", GetRestaurantProfileViewsApi.as_view(), name="get-restaurant-profile-views"),
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
    path(
        "menu/item/create/",
        CreateRestaurantMenuItemApi.as_view(),
        name="create-restaurant-menu-item",
    ),
    path(
        "menu/item/get/all/<int:restaurant_id>/",
        GetAllRestaurantMenuItemsApi.as_view(),
        name="get-all-restaurant-menu-items",
    ),
    path(
        "menu/item/get/<int:menu_item_id>/",
        GetRestaurantMenuItemInfo.as_view(),
        name="get-restaurant-menu-item-info",
    ),
    # path(
    #     "menu/item/get/all/<int:menu_id>/",
    #     GetAllRestaurantMenuItemsUnderMenuApi.as_view(),
    #     name="get-restaurant-menu-items-under-menu",
    # ),
    path(
        "menu/item/edit/<int:menu_item_id>/",
        EditRestaurantMenuItem.as_view(),
        name="edit-restaurant-menu-item",
    ),
    path(
        "menu/item/archive/<int:menu_item_id>/",
        ArchiveRestaurantMenuItemApi.as_view(),
        name="archive-restaurant-menu-item",
    ),
    path(
        "menu/item/delete/<int:menu_item_id>/",
        DeleteRestaurantMenuItemApi.as_view(),
        name="delete-restaurant-menu-item",
    ),
]
