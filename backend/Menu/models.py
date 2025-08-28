from django.db import models
from django.utils import timezone

class Menu(models.Model):
    """
    Top-level menu container, e.g., 'Main Menu', 'Footer Menu'
    """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"

    def __str__(self):
        return self.name


from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True, null=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        blank=True,
        null=True
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)  # Optional: to enable/disable menu items

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def get_children(self):
        return self.children.filter(is_active=True)

    def has_children(self):
        return self.children.filter(is_active=True).exists()