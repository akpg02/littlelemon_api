from django.shortcuts import render
from rest_framework.decorators import api_view  
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import status, viewsets
from user_app.serializers import RegistrationSerializer, CurrentUserSerializer
from user_app import models
from django.contrib.auth.models import User

# Create your views here.

@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        try:
            user = request.user
            if user.is_authenticated:
                user.auth_token.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['POST'])
def registration_view(request):
    
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        
        data ={}
        
        if serializer.is_valid():
            account = serializer.save()
            
            data['response'] = "Registration successful"
            data['username'] = account.username
            data['email'] = account.email
            
            token = Token.objects.get(user=account).key
            data['token'] = token
            
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET'])
def user_view(request):
    if request.user.is_authenticated: 
        serializer = CurrentUserSerializer(request.user)
        return Response(serializer.data)
    return Response(status=status.HTTP_401_UNAUTHORIZED)