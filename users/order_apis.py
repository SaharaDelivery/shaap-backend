from django.core.validators import MinValueValidator

from rest_framework import status
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from restaurants.models import MenuItem, Order, Restaurant
from restaurants.selectors import (
    get_all_order_items,
    get_all_orders_based_on_status,
    get_saved_user_addresses,
    get_user_order_history,
)
from users.services import (
    add_order_address,
    add_order_item,
    delete_order_item,
    edit_order_address,
    place_order,
    reduce_order_item_quantity,
)
from utils.serializer_utils import inline_serializer


class PlaceOrderApi(APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        restaurant = serializers.PrimaryKeyRelatedField(
            queryset=Restaurant.objects.all()
        )
        menu_item = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())

    def post(self, request):
        data = self.InputSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            place_order(
                user=request.user,
                **data.validated_data,
            )
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=data.errors)


class GetOrderBasedOnStatus(APIView):
    permission_classes = [IsAuthenticated]

    class OutputSerializer(serializers.Serializer):
        order_id = serializers.IntegerField()
        restaurant = inline_serializer(fields={"name": serializers.CharField()})
        status = serializers.CharField()
        total_price = serializers.DecimalField(max_digits=10, decimal_places=2)

    def get(self, request, order_status):
        pending_orders = get_all_orders_based_on_status(
            user=request.user, status=order_status
        )
        data = self.OutputSerializer(pending_orders, many=True)
        return Response(status=status.HTTP_200_OK, data=data.data)


class GetOrderHistoryApi(APIView):
    permission_classes = [IsAuthenticated]

    class OutputSerializer(serializers.Serializer):
        order_id = serializers.IntegerField()
        restaurant = inline_serializer(fields={"name": serializers.CharField()})
        total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
        date_created = serializers.DateTimeField()

    def get(self, request):
        order_history = get_user_order_history(user=request.user)
        data = self.OutputSerializer(order_history, many=True)
        return Response(status=status.HTTP_200_OK, data=data.data)


# NOTE: Needs further review
class GetOrderDetailsApi(APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        order_id = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class OutputSerializer(serializers.Serializer):
        order_id = serializers.IntegerField()
        restaurant = inline_serializer(fields={"name": serializers.CharField()})
        status = serializers.CharField()
        total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
        date_created = serializers.DateTimeField()
        order_items = serializers.SerializerMethodField()

        class OrderItemSerializer(serializers.Serializer):
            menu_item = inline_serializer(
                fields={
                    "name": serializers.CharField(),
                    "price": serializers.DecimalField(max_digits=10, decimal_places=2),
                }
            )
            quantity = serializers.IntegerField()

        def get_order_items(self, obj):
            order_items = get_all_order_items(order_id=obj.order_id)
            data = self.OrderItemSerializer(order_items, many=True)
            return data.data

    def get(self, request):
        data = self.InputSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            order_data = self.OutputSerializer(data.validated_data["order_id"])
            return Response(status=status.HTTP_200_OK, data=order_data.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=data.errors)


class AddOrderAddressApi(APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        address_1 = serializers.CharField()
        address_2 = serializers.CharField(required=False)
        phone_number = serializers.CharField()
        email = serializers.EmailField()
        saved = serializers.BooleanField()

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        address_1 = serializers.CharField()
        address_2 = serializers.CharField(required=False)
        phone_number = serializers.CharField()
        email = serializers.EmailField()
        saved = serializers.BooleanField()

    def post(self, request):
        data = self.InputSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            address = add_order_address(user=request.user, data=data.data)
            address_data = self.OutputSerializer(address)
            return Response(status=status.HTTP_201_CREATED, data=address_data.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=data.errors)


class GetSavedUserOrderAddressApi(APIView):
    permission_classes = [IsAuthenticated]

    class OutputSerializer(serializers.Serializer):
        address_1 = serializers.CharField()
        address_2 = serializers.CharField()
        phone_number = serializers.CharField()
        email = serializers.EmailField()

    def get(self, request):
        addresses = get_saved_user_addresses(user=request.user)
        data = self.OutputSerializer(addresses, many=True)
        return Response(status=status.HTTP_200_OK, data=data.data)


class EditOrderAddressApi(APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        address_1 = serializers.CharField(required=False)
        address_2 = serializers.CharField(required=False)
        phone_number = serializers.CharField(required=False)
        email = serializers.EmailField(required=False)
        saved = serializers.BooleanField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        address_1 = serializers.CharField()
        address_2 = serializers.CharField(required=False)
        phone_number = serializers.CharField()
        email = serializers.EmailField()
        saved = serializers.BooleanField()

    def put(self, request, address_id):
        data = self.InputSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            address = edit_order_address(
                user=request.user, data=data.data, address_id=address_id
            )
            address_data = self.OutputSerializer(address)
            return Response(status=status.HTTP_200_OK, data=address_data.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=data.errors)


class AddOrderItemApi(APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
        menu_item = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
        quantity = serializers.IntegerField(validators=[MinValueValidator(1)])

    def post(self, request):
        data = self.InputSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            add_order_item(**data.validated_data)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=data.errors)


class GetAllOrderItemsApi(APIView):
    permission_classes = [IsAuthenticated]

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        menu_item = inline_serializer(
            fields={
                "name": serializers.CharField(),
                "price": serializers.DecimalField(max_digits=10, decimal_places=2),
            }
        )
        quantity = serializers.IntegerField()

    def get(self, request, order_id):
        order_items = get_all_order_items(order_id=order_id)
        data = self.OutputSerializer(order_items, many=True)
        return Response(status=status.HTTP_200_OK, data=data.data)


class ReduceOrderItemQuantityApi(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, order_item_id):
        reduce_order_item_quantity(order_item_id=order_item_id)
        return Response(status=status.HTTP_200_OK)


class DeleteOrderItem(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, order_item_id):
        delete_order_item(order_item_id=order_item_id)
        return Response(status=status.HTTP_200_OK)
