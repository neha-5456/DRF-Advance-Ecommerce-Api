# urls.py
from django.urls import path
from .views import CheckoutView, PaymentView

urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("payment/<int:order_id>/", PaymentView.as_view(), name="payment"),
]


# curl -X POST http://127.0.0.1:8000/api/orders/checkout/ \
# -H "Authorization: Bearer <your_token>" \
# -H "Content-Type: application/json"

# curl -X POST http://127.0.0.1:8000/api/orders/payment/5/ \
# -H "Authorization: Bearer <your_token>" \
# -H "Content-Type: application/json" \
# -d '{"method": "COD"}'