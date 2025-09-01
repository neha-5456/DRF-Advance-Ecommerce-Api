from django.contrib import admin
from .models import User, PhoneOTP

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "is_verified", "is_staff", "is_active")
    search_fields = ("phone_number",)

@admin.register(PhoneOTP)
class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = ("phone", "otp", "created_at", "used", "attempts")
    search_fields = ("phone",)
