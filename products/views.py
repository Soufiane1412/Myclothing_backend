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
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue shopping on the current site.')]"))
        ).click()

        # wait for the page to load
        WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print(f"Page title: {driver.title}")


        # Progressive scroll and wait for content
        # last_height = driver.execute_script("return document.body.scrollHeight")
        # products_loaded = 0
        # max_scroll_attempts = 10
        # for scroll in range(max_scroll_attempts):
        #     print(f"\nScroll attempt {scroll + 1}/{max_scroll_attempts}")

        #     # Scroll down
        #     driver.execute_script("window.scrollTo(0, document.body)")
        #     time.sleep(3) # Wait for scroll to complete
            
            # # Wait for new images to load
            # try:
            #     WebDriverWait(driver, 10).until(
            #         lambda driver: len(driver.find_elements(By.CLASS_NAME, "product-cell__image")) > products_loaded
            #     )
            # except Exception as e:
            #     print(f"No new products loaded on scroll {scroll + 1}: {e}")
            # # Check if we've reached the bottom
            # new_height = driver.execute_script("return document.body.scrollHeight")
            # products_loaded = len(driver.find_element(By.CLASS_NAME, "product-cell__image"))
            # print(f"Products found after scroll: {products_loaded}")

            # if new_height == last_height:
            #     print("Reached bottom of page or no new content")
            #     break
            # last_height == new_height

        # Final wait for images to load
        print("Waiting for final images to load...")
        time.sleep(10)

        # Get final page_source  
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        selector = 'product-cell ss-t-center ss-bg-white product-cell--border'
        product_cards = soup.find_all('div', class_=selector)
        print(f"\nFound {len(product_cards)} total products")

        # Early return if no products
        if not product_cards:
            print("No products found with any selectors")
            return Response({
                'status': 'error',
                'message': 'No products found on the page',
                'products': [],
                'count': 0
            }, status=status.HTTP_404_NOT_FOUND)  # Use appropriate status code
        
        # Process products OUTSIDE the selector loop
        for index, product in enumerate(product_cards, 1):
            try:
                print(f"\nProcessing new product {index}/{len(product_cards)}")    

                # Extract img URL

                img_element = product.select_one('img.product-cell__image')
                if not img_element or not img_element.get('src'):
                    print("No valid image found")
                    continue
                img_url = img_element['src']
                if 'loading-tris.gif' in img_url or not img_url.startswith('http'):
                    print(f'Skipping invalid URL: {img_url}')
                    continue
                print(f"Found valid image URL: {img_url[:50]}...")
                
                # Find name with error handling
                name = "No name found"
                name_element = product.select_one('span[data-test="product-cell__product-name"]')
                if name_element:
                    name = name_element.text.strip()
                    print(f"Found name: {name}")
                
                # Find brand with error handling
                brand = "No brand found"
                brand_element = product.select_one('div.product-cell__brand-retailer')
                if brand_element:
                    brand = brand_element.text.strip()
                    print(f"Found brand: {brand}")

                # Find price with error handling
                price = "No price found"
                price_element = product.select_one('span.product-cell__price')
                if price_element:
                    price = price_element.text.strip()
                    print(f"Found price : {price}")

                if img_url or name: # Only add product if we found some data
                    product_cards = {
                        'img_url': img_url or 'No image available',
                        'name': name or 'No name available',
                        'brand': brand or 'No brand available',
                        'price': price or 'No price available'
                    }
                    products_data.append(product_cards)
                    print(f"Added product to list: {index}")

            except Exception as e:
                print(f"Error processing product {index}: {str(e)}")
                continue # Skip failed products
            
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



