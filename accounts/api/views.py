from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user_model


class RegisterView(APIView):
    def post(self, request):
        User = get_user_model()
        ser_data = UserSerializer(data=request.data)
        if ser_data.is_valid():
            User.objects.create_user(
                username=ser_data.validated_data['username'],
                password=ser_data.validated_data['password'],
            )
            return Response(ser_data.data)
        return Response(ser_data.errors)