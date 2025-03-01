from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.http import HttpRequest

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from oauth2_provider.views import TokenView
from oauth2_provider.contrib.rest_framework.permissions import OAuth2Authentication, TokenHasScope

from .models import User, Profile
from .serializers import UserSerializer, ProfileSerializer

import json

class UserViewSet(viewsets.ModelViewSet):
   authentication_classes = [OAuth2Authentication]
   permission_classes = [IsAuthenticated]
   # required_scopes = ['read', 'write']
   
   queryset = User.objects.all()
   serializer_class = UserSerializer

   @action(methods=['POST'], detail=False, url_path='signup', permission_classes=[AllowAny])
   def signUp(self, request):
      serializer = UserSerializer(data=request.data)

      if serializer.is_valid():
         serializer.save()
         print(f'Signed up: {request.data.get("username")}')
         return Response({"message": "Sign up successful!"}, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

   @action(methods=['POST'], detail=False, url_path='signin', permission_classes=[AllowAny])
   def signIn(self, request):
      username = request.data.get('username')
      password = request.data.get('password')

      if username and password:
         user = authenticate(request, username=username, password=password)
         
         if user is not None:
            login(request, user)
            
            token_request = HttpRequest()
            token_request.method = 'POST'
            token_request.POST = {
               'grant_type': 'password',
               'username': username,
               'password': password,
               'client_id': 'mXFmoA3VwA5JsZxmFjzNZWD4L6aK8cUHoy090eJl',
               'client_secret': 'oauth2',
            }
            
            token_view = TokenView.as_view()
            response = token_view(token_request)
            response_content = json.loads(response.content.decode('utf-8'))
            if response.status_code == 200:
               user_data = UserSerializer(user).data
               return Response({
                  "message": "Sign in successful!",
                  "access_token": response_content["access_token"],
                  "user_data": user_data
               }, status=status.HTTP_200_OK)
            else:
               return Response({"error": "Error generating token"}, status=response.status_code)
         else:
               return Response({"error": "Invalid credentials!"}, status=status.HTTP_401_UNAUTHORIZED)
      else:
         return Response({"error": "Username and password required!"}, status=status.HTTP_400_BAD_REQUEST)
      
class ProfileViewSet(viewsets.ModelViewSet):
   authentication_classes = [OAuth2Authentication]
   permission_classes = [IsAuthenticated]
   
   queryset = Profile.objects.all()
   serializer_class = ProfileSerializer