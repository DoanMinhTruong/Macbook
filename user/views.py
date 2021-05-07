from rest_framework.views import APIView
from rest_framework import authentication, permissions, status
from .models import MyUser
from .serializers import *
from django.http import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenVerifySerializer
import jwt, json
from django.core import serializers
from macbook import settings

def decode_jwt(request):
    class Temp:
        def __init__(self, is_admin):
            self.is_admin = is_admin
    try:
        data = jwt.decode(request.data['token'], settings.SECRET_KEY,  algorithms=['HS256'])
        user_id = data["user_id"]
        user = MyUser.objects.get(pk = user_id)
        return user
    except:
        # user = MyUser.objects.create(username = 'temp' , email = 'temp@gmail.com' ,is_admin = False)
        user = Temp(is_admin= False)
        return user


class ListUser(APIView):
    def post(self, request):
        try:
            user = decode_jwt(request)
            if user.is_admin:
                list_user = MyUser.objects.all()
                if not list_user:
                    return JsonResponse({
                        "message" : "dont have any user"
                    },status = status.HTTP_204_NO_CONTENT)
                return JsonResponse(list(MyUser.objects.all().values()), safe=False)
            return JsonResponse({
                "message": "not admin"
            } , status = status.HTTP_401_UNAUTHORIZED)
        except:
            return JsonResponse({
                "message": "error"
            }, status = status.HTTP_401_UNAUTHORIZED)

class UserRegister(APIView):
    def post(self, request):
        serializer = UserSerializers(data = request.data)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            user = serializer.save()
            return JsonResponse(
                {'message': 'Register Successfull!'}
            , status = status.HTTP_201_CREATED)
        return JsonResponse({
            'message': 'Register Fail !'
        }, status = status.HTTP_400_BAD_REQUEST)
class UserLogin(TokenObtainPairView):
    serializer_class = LoginSerializer

class UserDelete(APIView):
    def delete(self, request):
        user = decode_jwt(request)
        if(user.is_admin):
            try:
                getuser = MyUser.objects.get(username = request.data['username'])
            except:
                return JsonResponse({
                    "message": "user not exists"
                }, status = status.HTTP_404_NOT_FOUND)
            getuser.delete()
            return JsonResponse({
                "message": "delete successfull"
            } , status = status.HTTP_200_OK)
        return JsonResponse({
            "message": "you dont have any permissions"
        }, status = status.HTTP_400_BAD_REQUEST)

class UserUpdate(APIView):
    def put(self, request):
        user = decode_jwt(request)
        if(user.is_admin):
            serializer = UserSerializers(data = request.data['update'])
            if serializer.is_valid():
                serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
                user_up = serializer.update()
                return JsonResponse({
                    "message" : "update successful"
                }, status = status.HTTP_200_OK)
            return JsonResponse({
                "message" : "update fail"
            },status = status.HTTP_400_BAD_REQUEST)
        return JsonResponse({
            "message" : "error"
        } , status = status.HTTP_400_BAD_REQUEST)