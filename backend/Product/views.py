from django.shortcuts import render
from .serializers import CategorySerializers, ProductSerializer 
from .models import Category ,Product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins, generics , viewsets
from rest_framework import filters
from collections import defaultdict
from rest_framework.permissions import AllowAny





class CategoryListCreateView(mixins.ListModelMixin,mixins.CreateModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    permission_classes = [AllowAny] 
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
   
    def get(self, request, *args, **kwargs):
        if "pk" in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)  

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


    
    
class ProductListCreateView(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,  generics.GenericAPIView):
    permission_classes = [AllowAny] 
    def get_queryset(self):
        return Product.objects.all()[:8]
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']       # search by product name
    ordering_fields = ['price']  
    def get(self, request, *args, **kwargs):
        if "pk" in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)  

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProductViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = [AllowAny] 
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        grouped = defaultdict(list)

        for product in queryset:
            grouped[product.category.name].append(self.get_serializer(product).data)

        # Convert defaultdict to normal dict for response
        return Response(grouped)
 
 
    
class CategoryProductsView(APIView):
    permission_classes = [AllowAny] 
    def get(self, request, category_name):
        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=404)
        
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)    


#************New Arrival Product *************//
class NewArrivalProductList(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get_queryset(self):
        # Order by created_at descending, limit 8
        return Product.objects.all().order_by('-created_at')[:8]    
    
#************Featured Product *************//
class FeaturedProductList(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get_queryset(self):
        # Only featured products, limit 8
        return Product.objects.filter(is_featured=True).order_by('-created_at')[:8]
    
#************Top Sell Product *************//   
class TopSellingProductList(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get_queryset(self):
        # Order by total_sales descending, limit 8
        return Product.objects.filter(stock__gt=0).order_by('-total_sales')[:8]
    
    