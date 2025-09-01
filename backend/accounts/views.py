from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RequestOTPSerializer, VerifyOTPSerializer
from .models import PhoneOTP, User
from .utils import generate_otp, send_otp_via_sms
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

class RequestOTPView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RequestOTPSerializer

    def post(self, request, *args, **kwargs):
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        phone = s.validated_data["phone"]

        # Rate limiting simple example: check recent OTPs
        recent = PhoneOTP.objects.filter(phone=phone, created_at__gte=timezone.now()-timezone.timedelta(minutes=1))
        if recent.exists():
            return Response({"detail": "OTP already sent recently. Wait a bit."}, status=429)

        otp = generate_otp()
        PhoneOTP.objects.create(phone=phone, otp=otp)
        send_otp_via_sms(phone, otp)
        return Response({"detail": "OTP sent"}, status=status.HTTP_200_OK)


class VerifyOTPView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyOTPSerializer

    def post(self, request, *args, **kwargs):
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        phone = s.validated_data["phone"]
        otp = s.validated_data["otp"]

        try:
            latest = PhoneOTP.objects.filter(phone=phone, used=False).latest("created_at")
        except PhoneOTP.DoesNotExist:
            return Response({"detail": "No OTP request found"}, status=400)

        if latest.is_expired(minutes=5):
            return Response({"detail": "OTP expired"}, status=400)

        if latest.otp != otp:
            latest.attempts += 1
            latest.save()
            return Response({"detail": "Invalid OTP"}, status=400)

        # mark used
        latest.used = True
        latest.save()

        # get or create user
        user, created = User.objects.get_or_create(phone_number=phone)
        user.is_verified = True
        user.save()

        # issue JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {"phone_number": user.phone_number}
        }, status=200)


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Expect client to send refresh token to blacklist it
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token required"}, status=400)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # requires token_blacklist app
            return Response({"detail": "Logged out"}, status=200)
        except Exception:
            return Response({"detail": "Invalid token"}, status=400)


# Example protected endpoint
from rest_framework.views import APIView
class MeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        return Response({"phone_number": user.phone_number, "is_verified": user.is_verified})
