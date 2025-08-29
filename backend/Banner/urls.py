from django.urls import path
from .views import BannerListAPI

urlpatterns = [
    path('banners/', BannerListAPI.as_view(), name='banner'),
 
]
