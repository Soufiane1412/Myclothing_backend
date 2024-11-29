from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class meta:
        model = Product
        fields = ['name', 'brand', 'price', 'image_url']


class MyTokenObtainPairSerializer(TokenObtainPariSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username

        return token