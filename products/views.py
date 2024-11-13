from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from django.http import JsonResponse
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())


@api_view(['GET'])
def product_list(request):
    product = Product.objects.all()
    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data)<

def scrape_images(request): 
    driver = webdriver.Firefox()
    driver.get('https://www.ralphlauren.fr/')
    try:
        cookie_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='AUTORISER TOUS LES COOKIES']"))
        )
        cookie_button.click()
    except:
        print("NO cookie consent popup found, proceeding...")
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    products_images = []
    product_images =[]
    for a_tag in soup.find_all('a'):
        img_tag = a_tag.find('img')
        if img_tag.get('src'):
            product_images.append(img_tag)
            if product_images:
                products_images.append(product_images)

    driver.quit()
    return JsonResponse(products_images, safe=False)