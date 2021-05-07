from rest_framework import serializers
from .models import Mac
class MacSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mac
        fields = ['name' , 'img' , 'price' , 'rating' , 'informations']