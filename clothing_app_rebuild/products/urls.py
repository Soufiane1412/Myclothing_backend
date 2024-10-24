from django.urls import path
from .views import product_list, scrape_images

urlpatterns =[
    path('products/', product_list, name='product-list'),
    path('scrape/', scrape_images, name='scrape-images'),
]