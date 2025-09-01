from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Phone number required")
        phone_number = self.normalize_phone(phone_number)
        user = self.model(phone_number=phone_number, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(phone_number, password, **extra_fields)

    def normalize_phone(self, phone):
        return phone.strip()


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=20, unique=True)

    # ✅ Extra fields
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    profile_pic = models.ImageField(upload_to="profiles/", blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    adhar_card = models.FileField(upload_to="adhar_cards/", blank=True, null=True)

    # ✅ Permissions & status
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email"]  # email optional but good for superuser

    def __str__(self):
        return self.phone_number

    @property
    def full_name(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip()


class PhoneOTP(models.Model):
    phone = models.CharField(max_length=20, db_index=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    attempts = models.IntegerField(default=0)
    used = models.BooleanField(default=False)

    def is_expired(self, minutes=5):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=minutes)

    def __str__(self):
        return f"{self.phone} - {self.otp} - used:{self.used}"
