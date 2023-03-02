from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.validators import UniqueValidator
from utils.authtoken_serializer import AuthTokenSerializer

from knox.models import AuthToken

from users.models import CustomUser
from users.services import (
    create_user,
    disable_user_account,
    edit_user_account,
    login_user,
)
from utils.serializer_utils import inline_serializer


class RegisterUserApi(APIView):
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


class GetUserAccountApi(APIView):
    permission_classes = [IsAuthenticated]

    class OutputSerializer(serializers.Serializer):
        first_name = serializers.CharField()
        last_name = serializers.CharField()
        username = serializers.CharField()
        email = serializers.EmailField()
        phone_number = serializers.CharField()
        # adresses = inline_serializer(fields={})

    def get(self, request):
        try:
            data = self.OutputSerializer(request.user)
            return Response(data=data.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=e)


class EditUserAccountApi(APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        first_name = serializers.CharField(required=False)
        last_name = serializers.CharField(required=False)
        username = serializers.CharField(
            required=False,
            validators=[UniqueValidator(queryset=CustomUser.objects.all())],
        )
        email = serializers.EmailField(
            required=False,
            validators=[UniqueValidator(queryset=CustomUser.objects.all())],
        )
        phone_number = serializers.CharField(required=False)

    def put(self, request):
        data = self.InputSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            edit_user_account(user=request.user, data=data.data)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=data.errors)


class DisableUserAccountApi(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        disable_user_account(user=request.user)
        return Response(status=status.HTTP_200_OK)


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
