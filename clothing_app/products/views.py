from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serialisers import ProductSerializer
from django.http import JsonResponse
from selenium import webdriver
from bs4 import BeautifulSoup

@api_view(['GET'])
def product_list(request):
    product = Product.objects.all()
    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data)

def scrape_images():
    driver = webdriver.Firefox()
    driver.get('https://www.gucci.com/us/en/ca/men/shoes-for-men/loafers-for-men-c-men-shoes-moccasins-and-loafers')
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    images =[img.get('src') for img in soup.find_all('img')]
    driver.quit()
    return JsonResponse(images)