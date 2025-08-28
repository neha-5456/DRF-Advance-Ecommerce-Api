from django.contrib import admin
from .models import Product, Category , Tag , Brand ,Attribute, ProductImage , AttributeValue , ProductVariation

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price")   # jo bhi fields dikhani ho
    search_fields = ("name",)
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")   # jo bhi fields dikhani ho
    search_fields = ("name",)
  

    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")   # jo bhi fields dikhani ho
    search_fields = ("name",)  
    
@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")   # jo bhi fields dikhani ho
    search_fields = ("name",)  
    
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name")   # jo bhi fields dikhani ho
    search_fields = ("name",)  
    
@admin.register(ProductImage)
class ProductImage(admin.ModelAdmin):
    list_display = ("id", "product")   # jo bhi fields dikhani ho
    search_fields = ("product",)     
    
@admin.register(AttributeValue)
class AttributeValue(admin.ModelAdmin):
    list_display = ("id", "attribute", "value")   # jo bhi fields dikhani ho
    search_fields = ("attribute",)     
    
@admin.register(ProductVariation)
class ProductVariation(admin.ModelAdmin):
    list_display = ("id", "product","is_active")   # jo bhi fields dikhani ho
    search_fields = ("product",)     
        
    