from django.urls import path
from .views import product_list, scrape_images

# Token JWT import 
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns =[
    path('', product_list, name='product-list'),
    path('scrape/', scrape_images, name='scrape-images'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]