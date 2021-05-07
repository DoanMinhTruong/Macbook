from django.urls import path
from .views import *
urlpatterns = [
    path('' , ListMac.as_view() , name = 'listmac'),
    path('add/' , AddMac.as_view() , name = 'addmac'),
    path('delete/', DeleteMac.as_view() , name = 'delete'),
]