# urls.py
from django.urls import path
from .views import CartView, AddToCartView, UpdateCartItemView

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/add/", AddToCartView.as_view(), name="cart-add"),
    path("cart/item/<int:pk>/", UpdateCartItemView.as_view(), name="cart-item-update-delete"),
]
