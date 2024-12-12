import time
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.models import User

# DRF imports
from rest_framework import status
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

# websocket imports
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# JWT imports
from .serializers import MyTokenObtainPairView, MyTokenObtainPairSerializer

# Authentication import 
from django.contrib.auth.models import User



################################ Product ################################

@api_view(['GET'])
def product_list(request):
    product = Product.objects.all()
    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)  # Use status codes from DRF


################################ Scraping logic ################################

@csrf_exempt
@api_view(['GET'])
def scrape_images(request): 
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)

    women_dresses = []
    women_handbags = []
    men_jackets = []
    men_shoes = []

    try:
        # FIRST SCRAPING WOMEN'S DRESS

        print("Starting scraping process one...")
        driver.get('https://www.shopstyle.com/browse/dresses?sort=Popular')
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
        max_attempts = 5

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
                const mainImage = product.querySelector('img.product-cell__image');
                const altImage = product.querySelector('img.product-cell__image--alternate');
                
                const imgUrls = [];
                        if (mainImage && mainImage.src.includes('shopstyle-cdn.com')) {
                                imgUrls.push(mainImage.src)
                            };
                        if (altImage && altImage.src.includes('shopstyle-cdn.com')) {
                                imgUrls.push(altImage.src)
                            };                                        
                const name = product.querySelector('[data-test="product-cell__product-name"]');
                const brand = product.querySelector('.product-cell__brand-retailer');
                const price = product.querySelector('.product-cell__price');
                                            
                return {
                img_urls: imgUrls,
                name: name ? name.textContent.trim() : null,
                brand: brand ? brand.textContent.trim() : null,
                price: price ? price.textContent.trim() : null                                 
                }
            }).filter(product => 
                    product.img_urls &&
                    product.img_urls.length > 0 &&
                    product.name &&
                    product.brand &&
                    product.price
                );
        """)
        # Process the result
        for product in products:
            if product['img_urls']: #Only add products with valid URLs
                women_dresses.append({
                    'img_urls': product['img_urls'],
                    'name': product['name'] or 'No name available',
                    'brand': product['brand'] or 'No brand available',
                    'price': product['price'] or 'No price available'
                })
                print(f"Added product: {product['name']} - {product['brand']} - {product['price']}")
                print(f"Images: {product['img_urls']}") # print img_urls for debugging
        


        # SECOND SCRAPING WOMEN'S BAGS

        print("Starting scraping process two...")
        driver.get('https://www.shopstyle.com/browse/handbags?sort=Popular')
        print("page loaded successfully")

        # Handle cookie consent popup
        try:

            WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue shopping on the current site.')]"))
            ).click()
            print("Cookie consent accepted")
        except TimeoutException:
            print("No cookie consent popup found, continuing...")
        
        # Improved scrolling for images to load
        scroll_attempts = 0
        max_attempts = 5

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
                const mainImage = product.querySelector('img.product-cell__image');
                const altImage = product.querySelector('img.product-cell__image--alternate');
                                         
                        const imgUrls = []
                            if (mainImage && mainImage.src.includes('shopstyle-cdn.com')) {
                            imgUrls.push(mainImage.src)             
                            };
                            if (altImage && altImage.src.includes('shopstyle-cdn.com')) {
                                imgUrls.push(altImage.src)
                            };
                const name = product.querySelector('[data-test="product-cell__product-name"]');
                const brand = product.querySelector('.product-cell__brand-retailer');
                const price = product.querySelector('.product-cell__price');
                                            
                return {
                img_urls: imgUrls,
                name: name ? name.textContent.trim() : null,
                brand: brand ? brand.textContent.trim() : null,
                price: price ? price.textContent.trim() : null                                 
                }
            }).filter(product => 
                    product.img_urls &&
                    product.img_urls.length > 0 &&
                    product.name &&
                    product.brand &&
                    product.price 
                );
        """)

        # Process the result
        for product in products:
            if product['img_urls']: #Only add products with valid URLs
                women_handbags.append({
                    'img_urls': product['img_urls'],
                    'name': product['name'] or 'No name available',
                    'brand': product['brand'] or 'No brand available',
                    'price': product['price'] or 'No price available'
                })
                print(f"Added product: {product['name']} - {product['brand']} - {product['price']}")
                print(f"Added images_urls: {product['img_urls']}")


        
        # THIRD SCRAPING MEN'S JACKETS

        print("Starting scraping process three...")
        driver.get('https://www.shopstyle.com/browse/mens-light-jackets?sort=Popular')
        print("page loaded successfully")

        # Handle cookie consent popup
        try:

            WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue shopping on the current site.')]"))
            ).click()
            print("Cookie consent accepted")
        except TimeoutException:
            print("No cookie consent popup found, continuing...")
        
        # Improved scrolling for images to load
        scroll_attempts = 0
        max_attempts = 5

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
                const mainImage = product.querySelector('img.product-cell__image');
                const altImage = product.querySelector('img.product-cell__image--alternate');
                                         
                        const imgUrls = [];
                            if (mainImage && mainImage.src.includes('shopstyle-cdn.com')) {
                            imgUrls.push(mainImage.src)    
                                };
                            if (altImage && altImage.src.includes('shopstyle-cdn.com')) {
                                imgUrls.push(altImage.src)        
                                };
                                         
                const name = product.querySelector('[data-test="product-cell__product-name"]');
                const brand = product.querySelector('.product-cell__brand-retailer');
                const price = product.querySelector('.product-cell__price');
                                            
                return {
                img_urls: imgUrls,
                name: name ? name.textContent.trim() : null,
                brand: brand ? brand.textContent.trim() : null,
                price: price ? price.textContent.trim() : null                                 
                }
            }).filter(product => 
                    product.img_urls &&
                    product.img_urls.length > 0 &&
                    product.name &&
                    product.brand &&
                    product.price                        
                );
        """)

        # Process the result
        for product in products:
            if product['img_urls']: #Only add products with valid URLs
                men_jackets.append({
                    'img_urls': product['img_urls'],
                    'name': product['name'] or 'No name available',
                    'brand': product['brand'] or 'No brand available',
                    'price': product['price'] or 'No price available'
                })
                print(f"Added product: {product['name']} - {product['brand']} - {product['price']}")
                print(f"Found images: {product['img_urls']}")


        # FOURTH scraping process

        print("Starting scraping process four...")
        driver.get('https://www.shopstyle.com/browse/mens-shoes?sort=Popular')
        print("page loaded successfully")

        # Handle cookie consent popup
        try:

            WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue shopping on the current site.')]"))
            ).click()
            print("Cookie consent accepted")
        except TimeoutException:
            print("No cookie consent popup found, continuing...")
        
        # Improved scrolling for images to load
        scroll_attempts = 0
        max_attempts = 5

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
                const mainImage = product.querySelector('img.product-cell__image');
                const altImage = product.querySelector('img.product-cell__image--alternate');
                            
                    const imgUrls = [];
                            if (mainImage && mainImage.src.includes('shopstyle-cdn.com')) {
                                imgUrls.push(mainImage.src)
                                };
                            if (altImage && altImage.src.includes('shopstyle-cdn.com')) {
                                imgUrls.push(altImage.src)
                                };
                    
                const name = product.querySelector('[data-test="product-cell__product-name"]');
                const brand = product.querySelector('.product-cell__brand-retailer');
                const price = product.querySelector('.product-cell__price');
                                            
                return {
                img_urls: imgUrls,
                name: name ? name.textContent.trim() : null,
                brand: brand ? brand.textContent.trim() : null,
                price: price ? price.textContent.trim() : null                                 
                }
            }).filter(product => 
                    product.img_urls &&
                    product.img_urls.length > 0 &&
                    product.name &&
                    product.brand &&
                    product.price 
                );
        """)

        # Process the result
        for product in products:
            if product['img_urls']: #Only add products with valid URLs
                men_shoes.append({
                    'img_urls': product['img_urls'],
                    'name': product['name'] or 'No name available',
                    'brand': product['brand'] or 'No brand available',
                    'price': product['price'] or 'No price available'
                })
                print(f"Added product: {product['name']} - {product['brand']} - {product['price']}")
                print(f"Found images: {product['img_urls']}")


        combined_data = {
            'women dresses': women_dresses,
            'women handbags': women_handbags,
            'men jackets': men_jackets,
            'men shoes': men_shoes
        }

        # Return response AFTER processing all products
        print(f"\nSuccesfully processed {len(combined_data)} products")
        return Response({
            'status': 'success',
            'count': len(combined_data),
            'products':combined_data
            }, status=status.HTTP_200_OK)
            
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


################################ websocket ################################
    
def my_view(request):

    # Send notification
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send) (
        'notifications', # Group name
        {
            'type': 'send_notification', # Maps to the consumer's method
            'message': 'Hello there, it is my first websocket message from Django 🙋🏻‍♂️📮'
        }
    )


@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # other user data (e.g., email)
    try:
        user = User.objects.create_user(username=username, password=password)
        #... optionally, you can add other data to the user object 
        return Response({'message': 'User registered usccessfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
