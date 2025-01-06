from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import Token
from .models import Product
from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    class meta:
        model = Product
        fields = ['name', 'brand', 'price', 'image_url']

# initialised the token serialiser
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username 

        return token
    
# Initialised the token view
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):

    """
    UserSerializer converts User model instances to/from JSON.
    It inherits from ModelSerializer which provides default create/update operations
    """
    # write_only = True ensures password isn't included in responses
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    
    def create(self, validated_data):
        # Never store raw passwords! Django handles hashing
        user = user.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''), # Email optional
            password=validated_data['password']
        )