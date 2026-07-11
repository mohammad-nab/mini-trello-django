from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response


class RegisterView(APIView):
    def post(self, request):
        ser_data = UserSerializer(data=request.data)
        if ser_data.is_valid(raise_exception=True):
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)




