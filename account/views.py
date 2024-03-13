
from django.shortcuts import render
from rest_framework.decorators import  api_view
from rest_framework.response import Response
from django.contrib.auth import  authenticate
from .jwt_auth import create_access_token, decode_access_token, create_refresh_token, decode_refresh_token

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        return Response({'access_token': access_token, 'refresh_token': refresh_token})
    else:
        return Response({'error': 'Invalid credentials'})


