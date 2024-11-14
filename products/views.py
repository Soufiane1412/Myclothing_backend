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
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@api_view(['GET'])
def product_list(request):
    product = Product.objects.all()
    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data)

def scrape_images(request): 
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    try:
        print("Starting scraping process...")
        driver.get('https://www.ralphlauren.fr/')
        print("page loaded successfully")

        # wait for the page to load
        WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print(f"Page title: {driver.title}")
        # try different selector for the cookie button
        try:
            # first attempt original selector
            cookie_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='AUTORISER TOUS LES COOKIES']"))
            )
            cookie_button.click()
            print("Found and clicked cookie button with first selector")
        except:
            try:
                # Second attempt - try ID or class
                cookie_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "#onetrust-accept-btn-handler"))
                )
                cookie_button.click()
                print("Found and clicked cookie button with second selector")
            except Exception as e:
                print(f"Cookie button not found: {str(e)}")



        # Rest of the scraping logic
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        products_images = []
        for img_tag in soup.find_all('img'):
            if img_tag.get('src'):
                products_images.append({
                    'src': img_tag['src'],
                    'alt': img_tag('alt', '')
                })
        return JsonResponse({'images': products_images})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        driver.quit()