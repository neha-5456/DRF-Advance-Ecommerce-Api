# orders/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Cart.models import Cart
from .models import Order, OrderItem, Payment


class CheckoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart = user.cart  # OneToOne relation se direct mil jayega
        if not cart.items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Order create
        order = Order.objects.create(user=user, total_amount=cart.total_price)

        # 2. Cart items → Order items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

        # 3. Payment object create (pending)
        Payment.objects.create(order=order, amount=order.total_amount)

        # 4. Cart clear
        cart.items.all().delete()

        return Response({
            "message": "Order created successfully",
            "order_id": order.id,
            "total": order.total_amount,
            "payment_status": "pending"
        })


from rest_framework.views import APIView

class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        payment = order.payment
        # For now: mark as success
        payment.status = "success"
        payment.payment_method = request.data.get("method", "COD")
        payment.transaction_id = "TXN123456"  # In real integration, gateway se aata hai
        payment.save()

        # Update order status
        order.status = "paid"
        order.save()

        return Response({"message": "Payment successful", "order_status": order.status})
