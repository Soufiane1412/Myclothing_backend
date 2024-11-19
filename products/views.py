import time
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# DRF imports
from rest_framework.decorators import api_view
from rest_framework.response import Response  # We'll use this instead of JsonResponse
from rest_framework import status  # Add this for HTTP status codes

# Models and serializers
from .models import Product
from .serializers import ProductSerializer

# Scraping imports

from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@api_view(['GET'])
def product_list(request):
    product = Product.objects.all()
    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)  # Use status codes from DRF

@csrf_exempt
@api_view(['GET'])
def scrape_images(request): 
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    products_data = []

    try:
        print("Starting scraping process...")
        driver.get('https://www.shopstyle.com/browse/dresses')
        print("page loaded successfully")

        # Handle cookie consent popup
        try:

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue shopping on the current site.')]"))
            ).click()
            print("Cookie consent accepted")
        except TimeoutException:
            print("No cookie consent popup found, continuing...")
        
        # Improved scrolling for images to load
        scroll_attempts = 0
        max_attempts = 3

        while scroll_attempts < max_attempts:
            # scroll down 

            driver.execute_script('window.scrollBy(0, 800);') # scroll by fixed amount
            time.sleep(2) # Wait for content to load

            try:
                # Wait for new products to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img.product-cell__image[src*='shopstyle-cdn.com']"))
                )
                print(f"Scroll attempt {scroll_attempts + 1}: Products loaded")
            except TimeoutException:
                print(f"Scroll attempt {scroll_attempts + 1}: No new products loaded")

            scroll_attempts += 1

        # Final wait for all images  
        time.sleep(3)

        # Use JS to get fully loaded products
        products = driver.execute_script("""
        return Array.from(document.querySelectorAll('.product-cell')).map(product => {
            const img = product.querySelector('img.product-cell__image');
            const name = product.querySelector('[data-test="product-cell__product-name"]');
            const brand = product.querySelector('.product-cell__brand-retailer');
            const price = product.querySelector('.product-cell__price');
                                         
        return {
         img_url: img ? img.src : null,
         name: name ? name.textContent.trim() : null,
         brand: brand ? brand.textContent.trim() : null,
         price: price ? price.textContent.trim() : null                                 
        }
    }).filter(product => 
            product.img_url &&
            product.img_url.includes('shopstyle-cdn.com')
        );
    """)
        # Process the result
        for product in products:
            if product['img_url']: #Only add products with valid URLs
                products_data.append({
                    'img_url': product['img_url'],
                    'name': product['name'] or 'No name available',
                    'brand': product['brand'] or 'No brand available',
                    'price': product['price'] or 'No price available'
                })
                print(f"Added product: {product['name']} - {product['brand']} - {product['price']}")
            
        # Return response AFTER processing all products
        print(f"\nSuccesfully processed {len(products_data)} products")
        return Response({
            'status': 'success',
            'products': products_data,
            'count': len(products_data)
            }, status=status.HTTP_200_OK)  # Use appropriate status code
            
    except Exception as e:
        print(f"Error during main scraping: {str(e)}")
        return Response({
            'status': 'error',
            'message': str(e),
            'count': 0,
            'products': []
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # Use appropriate status code
    finally:
        driver.quit()



