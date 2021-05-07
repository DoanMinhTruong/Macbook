from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from .serializers import MacSerializer
from .models import Mac
from rest_framework import status
import jwt
from macbook import settings
from user.models import MyUser
# Create your views here.

def decode_jwt(request):
    try:
        data = jwt.decode(request.data['token'], settings.SECRET_KEY,  algorithms=['HS256'])
        user_id = data["user_id"]
        user = MyUser.objects.get(pk = user_id)
        return user
    except:
        user = MyUser.objects.create(is_admin = False)
        return user



class ListMac(APIView):
    def get(self, request ,format = None):
        list_mac = Mac.objects.all()
        if not list_mac:
            return JsonResponse({
                "message" : "dont have any macbook"
            }, status = status.HTTP_204_NO_CONTENT)
        return JsonResponse(list(list_mac.values()), safe=False)


class AddMac(APIView):
    def post(self, request):
        serializer = MacSerializer(data = request.data)
        if(serializer.is_valid()):
            mac = serializer.save()
            return JsonResponse({
                "message":"add successfull"
            }, status = status.HTTP_201_CREATED)
        return JsonResponse({
            "message": "add fail"
        }, status = status.HTTP_400_BAD_REQUEST)

class DeleteMac(APIView):
    def post(self , request):
        user = decode_jwt(request)
        if(user.is_admin):
            try:
                mac = Mac.objects.get(pk = request.data['mac_id'])
            except:
                return JsonResponse({
                    "message" : "dont have any mac with this id"
                }, status = status.HTTP_404_NOT_FOUND)
            mac.delete()
            return JsonResponse({
                "message": "delete successfull"
            } , status = status.HTTP_200_OK)
        return JsonResponse({
            "message": "you dont have any permissions"
        }, status = status.HTTP_400_BAD_REQUEST)