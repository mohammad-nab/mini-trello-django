from django.contrib.auth import get_user_model
from rest_framework import status
from django.contrib.auth import get_user_model , authenticate, login
from rest_framework.views import APIView
from .serializers import UserSerializer, LoginSerializer
from rest_framework.response import Response


class RegisterView(APIView):
    def post(self, request):
        ser_data = UserSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)

        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        ser_data = LoginSerializer(data=request.data)
        if ser_data.is_valid():
            username = ser_data.validated_data.get('username')
            password = ser_data.validated_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return Response({"message": "Login Succeed"}, status=status.HTTP_200_OK)

        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


