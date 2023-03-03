from rest_framework import status
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response


class PlaceOrderApi(APIView):
    class InputSerializer(serializers.Serializer):
        pass

    def post(self, request):
        pass
