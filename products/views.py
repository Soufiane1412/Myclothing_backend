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
    products_data = []

    try:
        print("Starting scraping process...")
        driver.get('https://www.shopstyle.com/browse/dresses')
        print("page loaded successfully")

        # wait for the page to load
        WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print(f"Page title: {driver.title}")
        # try different selector for the cookie button

        # Wait for grid products to load:
        try:
             WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product-cell ss-t-center ss-bg-white product-cell--border"))
            )
        except Exception as e:
            print(f'Timeout waiting for products: {str(e)}')
            # print page source for debugging 
            print('Current page source:')
            print(driver.page_source[:500]) # First 500 chars

        # cookie_button.click()
        # print("Found and clicked cookie button with selector")

        # Rest of the scraping logic
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        product_cards = []
        selectors = [
            'product-cell ss-t-center ss-bg-white product-cell--border',
            'data-test','product-cell',
            '_ngcontent-app-c3303513314',''
        ]

        for selector in selectors:
            try:
                product_cards = soup.find_all('div', class_=selector)
                print(f"Trying selector '{selector}': found{len(product_cards)} products")
                if product_cards:
                    break

                if not product_cards:
                    print("No products found with any selectors")
                    return JsonResponse({
                        'status': 'error',
                        'message': 'No products found on the page',
                        'products': [],
                        'count': 0
                    })
                for product in product_cards:
                    try:
                        # Print the HTML of each product card for debugging
                        print("product card HTML:")
                        print(product.prettify()[:200]) # First 200 chars
                        
                        # try multiple selectors for each element
                        img_url = None
                        img_selectors = [
                            'product-cell__image-wrapper ss-row ss-relative',
                            '_ngcontent-app-c3303513314',
                            'data-test',
                            'product-click'
                        ]
                        
                        



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

            return JsonResponse({
                'status': 'success',
                'products': products_data,
                'count': len(products_data)
            })
    except Exception as e:
        print(f'Main scraping error: {str(e)}')
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)



    def print_element_details(element):
        print("Tag:", element.name)
        print("Attributes:", element.attrs)
        print("Text content:", element.text.strip())

    # use in your code 
    for product in product_cards:
        name_element = product.find('span', attrs={'data-test': 'product-cell___product-name'})
        if name_element:
            print_element_details(name_element)

