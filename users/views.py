from django.shortcuts import render

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.validators import UniqueValidator
from users.authtoken_serializer import AuthTokenSerializer

from knox.models import AuthToken

from users.models import CustomUser
from users.services import create_user, login_user


class SignUpApi(APIView):
    class InputSerializer(serializers.Serializer):
        username = serializers.CharField(
            validators=[UniqueValidator(queryset=CustomUser.objects.all())]
        )
        email = serializers.EmailField(
            validators=[UniqueValidator(queryset=CustomUser.objects.all())]
        )
        first_name = serializers.CharField()
        last_name = serializers.CharField()
        phone_number = serializers.CharField()
        password = serializers.CharField()

    def post(self, request):
        data = self.InputSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            create_user(data=data.data)
            return Response(status=status.HTTP_201_CREATED)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginApi(APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()

    def post(self, request):
        data = AuthTokenSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            user = data.validated_data["user"]
            # AuthToken returns a tuple of (token, user) so we only get the token,
            _, token = AuthToken.objects.create(user)
            login_user(user=user)
            return Response(data={"token": token}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=data.errors)


class LogoutApi(APIView):
    def post(self, request):
        # deletes all the tokens the user has
        request.user.auth_token_set.all().delete()
        return Response(status=status.HTTP_200_OK)
