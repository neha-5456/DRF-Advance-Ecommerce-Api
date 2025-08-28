from django.urls import path
from .views import CategoryListCreateView, ProductListCreateView

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryListCreateView.as_view(), name='category-details'),
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductListCreateView.as_view(), name='product-detail')
]
