from django.urls import path
from .views import product_list, scrape_images, register

# Token JWT import 
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns =[
    path('api/products', product_list, name='product-list'),
    path('api/products/scrape/', scrape_images, name='scrape-images'),
    path('api/auth/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/register/', register,  name='register'),

]