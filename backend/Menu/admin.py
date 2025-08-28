from django.contrib import admin
from .models import Menu , MenuItem

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("id", "name")   # jo bhi fields dikhani ho
    search_fields = ("name",)
    
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name")   # jo bhi fields dikhani ho
    search_fields = ("name",)    