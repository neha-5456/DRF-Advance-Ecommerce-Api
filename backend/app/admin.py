from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock', 'category', 'created_at')
    search_fields = ('name', 'category')
    list_filter = ('category', 'created_at')
    ordering = ('-created_at',)
