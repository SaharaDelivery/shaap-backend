from django.urls import path

from restaurants.views import RegisterRestaurantApi

urlpatterns = [
    path("register/", RegisterRestaurantApi.as_view(), name="register-restaurant"),
    # path("get/", GetRestaurantInfoApi.as_view(), name="get-restaurant-info"),
    # path("get/all/", GetAllRestaurantsApi.as_view(), name="get-all-restaurants"),
    # path("get/filtered/", GetAllFilteredRestaurantsApi.as_view(), name="get-all-filtered-restaurants"),
    # path("edit/", EditRestaurantInfoApi.as_view(), name="edit-restaurant-info"),
    # path("delete/", DisableRestaurantApi.as_view(), name="disable-restaurant"),
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
