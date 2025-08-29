from django.urls import path
from .views import CategoryListCreateView, ProductListCreateView, ProductViewSet, CategoryProductsView,NewArrivalProductList,FeaturedProductList,TopSellingProductList


urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryListCreateView.as_view(), name='category-details'),
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductListCreateView.as_view(), name='product-detail'),
    path('category/', ProductViewSet.as_view({'get': 'list'}), name='all-category-products'),
    path('category/<str:category_name>/', CategoryProductsView.as_view(), name='category-products'),
    path('TopSellingProductList/', TopSellingProductList.as_view(), name='TopSellingProductList'),
    path('NewArrivalProductList/', NewArrivalProductList.as_view(), name='NewArrivalProductList'),
    path('FeaturedProductList/', FeaturedProductList.as_view(), name='FeaturedProductList'),
]
