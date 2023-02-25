from django.shortcuts import render

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.validators import UniqueValidator

from users.models import CustomUser
from users.services import create_user


class SignUpApi(APIView):
    class InputSerializer(serializers.Serializer):
        username = serializers.CharField(
            validators=[UniqueValidator(queryset=CustomUser.objects.all())]
        )
        email = serializers.EmailField(
            validators=[UniqueValidator(queryset=CustomUser.objects.all())]
        )
        password = serializers.CharField()

    def post(self, request):
        data = self.InputSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            create_user(data=data.data)
            return Response(status=status.HTTP_201_CREATED)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
