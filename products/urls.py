from django.urls import path
from .views import product_list, scrape_images, register

# Token JWT import 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns =[
    path('api/products/', product_list, name='product-list'),
    path('scrape/', scrape_images, name='scrape-images'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', register,  name='register'),

]