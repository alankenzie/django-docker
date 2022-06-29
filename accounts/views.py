from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import AccountSerializer
from drf_spectacular.utils import extend_schema

class AccountView(APIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer

    @extend_schema(
        responses={201: AccountSerializer}
    )
    def post(self, request):
        serializer = AccountSerializer(**request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(**serializer.validated_data)
        serialized = AccountSerializer(user)
        return Response(serialized.data)
