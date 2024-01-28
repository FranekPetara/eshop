from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

import datetime

from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# from .models import Profile
from .serializers import SignUpSerializer, UserSerializer



# Create your views here.

@api_view(['POST'])
def register(request):
    data = request.data

    user = SignUpSerializer(data = data)

    if user.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            user = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'],
                email = data['email'],
                username = data['email'],
                password = make_password(data['password'])
            )
            return Response({"details": "User is created"}, status=status.HTTP_201_CREATED)

        else:
            return Response({"details": "User already exist"}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(user.errors)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):

    user = UserSerializer(request.user, many = False)
    return Response(user.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):

    user = request.user
    data = request.data

    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.email = data['email']
    user.username = data['email']

    if data['password'] != "":
        user.password = make_password(data['password'])

    user.save()

    serializer = UserSerializer(user, many = False)

    return Response(serializer.data)

def get_current_host(request):
    protocol = request.is_secure() and "https" or "http"
    host = request.get_host()
    return f"{protocol}://{host}"


@api_view(['POST'])
def forgot_password(request):
    data = request.data

    user = get_object_or_404(User,email=data['email'])

    token = get_random_string(50)
    expire_date = datetime.datetime.now() + datetime.timedelta(minutes=10)

    user.profile.reset_password_token=token
    user.profile.reset_password_expire=expire_date

    user.profile.save()

    host = get_current_host(request)

    link = f"{host}/api/reset_password/{token}"
    body = f"Your password reset link is: {link}"

    send_mail(
        "Password refresh for eshop",
        body,
        "noreplay@eshop.com",
        [data["email"]]
    )

    return Response({"details": f"email with refresh password was  to {data['email']}"})


@api_view(['POST'])
def reset_password(request, token, ):
    data= request.data
    print()

    user = get_object_or_404(User, profile__reset_password_token=token)

    if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.datetime.now():
        return Response({"error": "Tocken is expired"}, status=status.HTTP_400_BAD_REQUEST)
    
    if data['password'] != data['confirmPassword']:
        return Response({"error": "pasword are not the same"}, status=status.HTTP_400_BAD_REQUEST)
    
    user.password = make_password(data['password'])
    user.profile.reset_password_token = ''
    user.profile.reset_password_expire = None

    user.profile.save()
    user.save()

    return Response({"details": f"password reset successfully."})