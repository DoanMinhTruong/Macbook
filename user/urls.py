from django.urls import path
from .views import *

urlpatterns = [
    path('', ListUser.as_view() , name = 'list'),
    path('register/', UserRegister.as_view() , name = 'register'),
    path('login/', UserLogin.as_view() , name = 'login'),
    path('delete/' , UserDelete.as_view() , name ='delete'),
    path('update/' , UserUpdate.as_view() , name = 'update'),
]