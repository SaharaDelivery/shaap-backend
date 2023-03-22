from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.validators import UniqueValidator

from knox.models import AuthToken
from restaurants.filters import filter_restaurants

from restaurants.models import Cuisine, Menu, Restaurant
from restaurants.selectors import (
    get_all_restaurant_menu_items,
    get_all_restaurants_with_cuisine,
    get_archived_restaurant_menus,
    get_all_restaurant_menus,
    get_all_restaurants,
    get_restaurant_info,
    get_restaurant_menu,
    get_restaurant_menu_item,
)
from restaurants.services import (
    archive_menu,
    archive_menu_item,
    create_menu,
    create_menu_item,
    delete_menu,
    delete_menu_item,
    disable_restaurant,
    login_restaurant_staff,
    register_restaurant,
    update_restaurant_info,
    update_restaurant_menu,
    update_restaurant_menu_item,
)

from utils.authtoken_serializer import AuthTokenSerializer
from utils.permission_utils import IsAdminUser, IsRestaurantAdmin
from utils.serializer_utils import inline_serializer


class RestaurantStaffLoginApi(APIView):
    def post(self, request):
        data = AuthTokenSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            user = data.validated_data["user"]
            # AuthToken returns a tuple of (token, user) so we only get the token,
            _, token = AuthToken.objects.create(user)
            login_restaurant_staff(user=user)
            return Response(data={"token": token}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=data.errors)


class RestaurantStaffLogoutApi(APIView):
    def post(self, request):
        # deletes all the tokens the user has
        request.user.auth_token_set.all().delete()
        return Response(status=status.HTTP_200_OK)


class RegisterRestaurantApi(APIView):
    permission_classes = [IsAdminUser]

    class InputSerializer(serializers.Serializer):
        # image = serializers.ImageField()
        name = serializers.CharField(
            validators=[UniqueValidator(queryset=Restaurant.objects.all())]
        )
        description = serializers.CharField()
        address = serializers.CharField()
        phone_number = serializers.CharField(max_length=12)
        email = serializers.EmailField(
            validators=[UniqueValidator(queryset=Restaurant.objects.all())]
        )
        opening_time = serializers.TimeField()
        closing_time = serializers.TimeField()

    def post(self, request):
        data = self.InputSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            register_restaurant(data=data.data, creator=request.user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=data.errors)


class GetRestaurantInfoApi(APIView):
    class OutputSerializer(serializers.Serializer):
        # image = serializers.ImageField()
        id = serializers.IntegerField()
        name = serializers.CharField()
        description = serializers.CharField()
        address = serializers.CharField()
        phone_number = serializers.CharField()
        email = serializers.EmailField()
        opening_time = serializers.TimeField()
        closing_time = serializers.TimeField()
        rating = serializers.DecimalField(max_digits=2, decimal_places=1)

    def get(self, request, id):
        # if object does not exist, it will raise a rest_exception
        restaurant = get_restaurant_info(id=id)
        data = self.OutputSerializer(restaurant)
        return Response(status=status.HTTP_200_OK, data=data.data)


class GetAllRestaurantsApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        # image = serializers.ImageField()
        name = serializers.CharField()
        description = serializers.CharField()
        cuisine = inline_serializer(
            many=True,
            read_only=True,
            fields={"id": serializers.IntegerField(), "name": serializers.CharField()},
        )
        opening_time = serializers.TimeField()
        closing_time = serializers.TimeField()
        rating = serializers.DecimalField(max_digits=2, decimal_places=1)

    def get(self, request):
        restaurants = get_all_restaurants()
        data = self.OutputSerializer(restaurants, many=True)
        return Response(status=status.HTTP_200_OK, data=data.data)


class GetRestaurantWithCuisineApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        # image = serializers.ImageField()
        name = serializers.CharField()
        description = serializers.CharField()
        cuisine = inline_serializer(
            many=True,
            read_only=True,
            fields={"id": serializers.IntegerField(), "name": serializers.CharField()},
        )
        opening_time = serializers.TimeField()
        closing_time = serializers.TimeField()
        rating = serializers.DecimalField(max_digits=2, decimal_places=1)

    def get(self, request, cuisine):
        restaurants = get_all_restaurants_with_cuisine(cuisine=cuisine)
        data = self.OutputSerializer(restaurants, many=True)
        return Response(status=status.HTTP_200_OK, data=data.data)


class GetAllFilteredRestaurantsApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        # image = serializers.ImageField()
        name = serializers.CharField()
        description = serializers.CharField()
        cuisine = inline_serializer(
            many=True,
            read_only=True,
            fields={"id": serializers.IntegerField(), "name": serializers.CharField()},
        )
        opening_time = serializers.TimeField()
        closing_time = serializers.TimeField()
        rating = serializers.DecimalField(max_digits=2, decimal_places=1)

    def get(self, request):
        filtered_restaurants = filter_restaurants(request.query_params)
        data = self.OutputSerializer(filtered_restaurants, many=True)
        return Response(data.data)


class EditRestaurantInfoApi(APIView):
    permission_classes = [IsRestaurantAdmin]

    class InputSerializer(serializers.Serializer):
        description = serializers.CharField(required=False)
        address = serializers.CharField(required=False)
        phone_number = serializers.CharField(required=False, max_length=12)
        opening_time = serializers.TimeField(required=False)
        closing_time = serializers.TimeField(required=False)

    def put(self, request, id):
        data = self.InputSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            update_restaurant_info(id=id, data=data.data)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=data.errors)


class ArchiveRestaurantApi(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, id):
        disable_restaurant(id=id)
        return Response(status=status.HTTP_200_OK)


class CreateRestaurantMenuApi(APIView):
    class InputSerializer(serializers.Serializer):
        restaurant = serializers.PrimaryKeyRelatedField(
            queryset=Restaurant.objects.all()
        )
        name = serializers.CharField(max_length=200)
        description = serializers.CharField()
        cuisine = serializers.PrimaryKeyRelatedField(queryset=Cuisine.objects.all())

    def post(self, request):
        data = self.InputSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            create_menu(data=data.data, creator=request.user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=data.errors)


class GetAllRestaurantMenusApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        cuisine = inline_serializer(fields={"name": serializers.CharField()})

    def get(self, request, restaurant_id):
        menus = get_all_restaurant_menus(restaurant_id=restaurant_id)
        data = self.OutputSerializer(menus, many=True)
        return Response(status=status.HTTP_200_OK, data=data.data)


class GetRestaurantMenuDetailsApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        restaurant = inline_serializer(fields={"name": serializers.CharField()})
        name = serializers.CharField()
        description = serializers.CharField()
        cuisine = inline_serializer(fields={"name": serializers.CharField()})

    def get(self, request, menu_id):
        menu = get_restaurant_menu(id=menu_id)
        data = self.OutputSerializer(menu)
        return Response(status=status.HTTP_200_OK, data=data.data)


class GetArchivedRestaurantMenusApi(APIView):
    permission_classes = [IsRestaurantAdmin]

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        cuisine = inline_serializer(fields={"name": serializers.CharField()})

    def get(self, request, restaurant_id):
        menus = get_archived_restaurant_menus(restaurant_id=restaurant_id)
        data = self.OutputSerializer(menus, many=True)
        return Response(status=status.HTTP_200_OK, data=data.data)


class ArchiveRestaurantMenuApi(APIView):
    permission_classes = [IsRestaurantAdmin]

    def put(self, request, menu_id):
        archive_menu(id=menu_id)
        return Response(status=status.HTTP_200_OK)


class DeleteRestaurantMenuApi(APIView):
    permission_classes = [IsRestaurantAdmin]

    def delete(self, request, menu_id):
        delete_menu(id=menu_id)
        return Response(status=status.HTTP_200_OK)


class EditRestaurantMenuApi(APIView):
    permission_classes = [IsRestaurantAdmin]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False, max_length=200)
        description = serializers.CharField(required=False)
        cuisine = serializers.PrimaryKeyRelatedField(
            queryset=Cuisine.objects.all(), required=False
        )

    def put(self, request, menu_id):
        data = self.InputSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            update_restaurant_menu(id=menu_id, data=data.data)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=data.errors)


class CreateRestaurantMenuItemApi(APIView):
    permission_classes = [IsRestaurantAdmin]

    class InputSerializer(serializers.Serializer):
        menu = serializers.PrimaryKeyRelatedField(queryset=Menu.objects.all())
        name = serializers.CharField(max_length=200)
        description = serializers.CharField()
        price = serializers.DecimalField(max_digits=10, decimal_places=2)

    def post(self, request):
        data = self.InputSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            create_menu_item(data=data.data, creator=request.user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=data.errors)


class GetAllRestaurantMenuItemsApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        description = serializers.CharField()
        price = serializers.DecimalField(max_digits=10, decimal_places=2)

    def get(self, request, menu_id):
        items = get_all_restaurant_menu_items(id=menu_id)
        data = self.OutputSerializer(items, many=True)
        return Response(status=status.HTTP_200_OK, data=data.data)


class GetRestaurantMenuItemInfo(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        description = serializers.CharField()
        price = serializers.DecimalField(max_digits=10, decimal_places=2)

    def get(self, request, menu_item_id):
        item = get_restaurant_menu_item(id=menu_item_id)
        data = self.OutputSerializer(item)
        return Response(status=status.HTTP_200_OK, data=data.data)


class EditRestaurantMenuItem(APIView):
    permission_classes = [IsRestaurantAdmin]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False, max_length=200)
        description = serializers.CharField(required=False)
        price = serializers.DecimalField(
            max_digits=10, decimal_places=2, required=False
        )

    def put(self, request, menu_item_id):
        data = self.InputSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            update_restaurant_menu_item(id=menu_item_id, data=data.data)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=data.errors)


class ArchiveRestaurantMenuItemApi(APIView):
    permission_classes = [IsRestaurantAdmin]

    def put(self, request, menu_item_id):
        archive_menu_item(id=menu_item_id)
        return Response(status=status.HTTP_200_OK)


class DeleteRestaurantMenuItemApi(APIView):
    permission_classes = [IsRestaurantAdmin]

    def delete(self, request, menu_item_id):
        delete_menu_item(id=menu_item_id)
        return Response(status=status.HTTP_200_OK)
