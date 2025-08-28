from django.shortcuts import render
from .serializers import CategorySerializers, ProductSerializer 
from .models import Category ,Product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins, generics
from rest_framework import filters

class CategoryListCreateView(mixins.ListModelMixin,mixins.CreateModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    def get(self, request, *args, **kwargs):
        if "pk" in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)  

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


    
    
class ProductListCreateView(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,  generics.GenericAPIView):
    queryset = Product.objects.all()
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
