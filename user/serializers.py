from rest_framework import serializers
from .models import MyUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenVerifySerializer
from rest_framework_simplejwt.tokens import UntypedToken

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['email' , 'username' , 'password']
        extra_kwargs = {'password': {'write_only': True}}

class LoginSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': {
            'message': 'Dont have any user',
        }
    }   
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        del data['refresh'] , data['access']
        data['message'] = 'Login successful'
        data['data'] = {}

        # Add extra responses here
        data['data']['username'] = self.user.username        

        data['data']['token'] = {}
        data['data']['token']['refresh'] = str(refresh)
        data['data']['token']['access'] = str(refresh.access_token)
        return data



