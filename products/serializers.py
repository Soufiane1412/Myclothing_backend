from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class meta:
        model = Product
        fields = ['name', 'brand', 'price', 'image_url']