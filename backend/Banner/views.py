from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Banner
from .serializers import BannerSerializer

class BannerListAPI(APIView):
    # Set permissions at the class level
    permission_classes = [AllowAny]

    def get(self, request):
        # Fetch active banners
        banners = Banner.objects.filter(is_active=True).order_by('display_order', '-created_at')
        serializer = BannerSerializer(banners, many=True, context={'request': request})
        return Response(serializer.data, status=200)
