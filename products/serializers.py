from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import Token
from .models import Product

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
