from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


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



def product_list(request):
    product = Product.objects.all()
    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data)

@csrf_exempt
def scrape_images(request): 
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    try:
        print("Starting scraping process...")
        driver.get('https://www.shopstyle.com/browse/dresses')
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
    except:



        # Rest of the scraping logic
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        products_data = []

        product_cards = soup.find_all('div', class_='products-list__item products-list__cell ng-star-inserted')

        for product in product_cards:
            try:
                # Extract image URL
                img_tag = product.find('img', class_='product-cell__image product-cell__image--has-alternate')
                img_url = img_tag.get('src') if img_tag else ''

                # Extract product name
                name_element = product.find('span', attrs={'data-test':'product-cell__product-name'})
                if not name_element:
                    name_element = product.find('span', attrs={'_ngcontent-app-c330351314': ''})
                    name = name_element.text.strip() if name_element else ''
                

                # Extract brand tag
                brand_element = product.find('span', class_="ss-t-text-ellipsis ss-w-full")
                if not brand_element:
                    brand_element = product.find('span', attrs={"_ngcontent-app-c3303513314":""})
                    brand = brand_element.text.strip() if brand_element else 'unknown'

                # Extract element price
                element_price = product.find('span', class_='product-cell__price ss-red ng-star-inserted')
                if not element_price:
                    element_price = product.find('span', attrs={'data-test':'product-cell__price'})
                    price = element_price.text.strip() if element_price else 'FREE 🫰🏽'

                # Debug prints
                print(f"Found name: {name}")
                print(f"Found brand: {brand}")

                products_data.append({
                    'img_url': img_url,
                    'name': name,
                    'brand': brand,
                    'price': price
                })
            except Exception as e:
                print(f"Error processing product: {str(e)}")
                continue


    def print_element_details(element):
        print("Tag:", element.name)
        print("Attributes:", element.attrs)
        print("Text content:", element.text.strip())

    # use in your code 
    for product in product_cards:
        name_element = product.find('span', attrs={'data-test': 'product-cell___product-name'})
        if name_element:
            print_element_details(name_element)

