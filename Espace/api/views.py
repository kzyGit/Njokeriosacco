from rest_framework import generics
from .serializers import TokenSerializer, RegistrationSerializer
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import (IsAdminUser, IsAuthenticated, AllowAny)
from django.contrib.auth import login, authenticate
from .models import User

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class Users(generics.ListCreateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        user = request.data
        
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        response = {
            "message": "User registered successfully",
            "user_info": serializer.data
            }
        return Response(response,status=status.HTTP_201_CREATED)

class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class=RegistrationSerializer
    permission_classes=(IsAuthenticated, IsAdminUser,)


class LoginView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")

        if not username or not password:
            response = Response({
                'message':"Ensure to give both your username and password"
            })
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                serializer = TokenSerializer(data={
                    "token": jwt_encode_handler(jwt_payload_handler(user)),
                    })

                serializer.is_valid()
                response = Response({
                    'message':"Logged in successfully",
                    'token':serializer.data['token'],
                })
            else:
                response = Response({'error':"Invalid login credentials"},status=status.HTTP_401_UNAUTHORIZED)
        return response


