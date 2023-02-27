from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.validators import UniqueValidator

from restaurants.models import Restaurant
from restaurants.services import register_restaurant

from utils.permission_utils import IsAdminUser


class RegisterRestaurantApi(APIView):
    permission_classes = [IsAdminUser]

    class InputSerializer(serializers.Serializer):
        # image = serializers.ImageField()
        name = serializers.CharField(
            validators=[UniqueValidator(queryset=Restaurant.objects.all())]
        )
        description = serializers.CharField()
        address = serializers.CharField()
        phone_number = serializers.CharField()
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
