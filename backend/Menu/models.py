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


class MenuItem(models.Model):
    """
    Individual menu items, supporting nested menus.
    """
    menu = models.ForeignKey(Menu, related_name="items", on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self", blank=True, null=True, related_name="children", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    url = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Enter a relative URL or external link (e.g., /about/ or https://example.com)"
    )
    link_type_choices = [
        ("internal", "Internal Page"),
        ("external", "External URL"),
        ("category", "Category"),
        ("product", "Product"),
    ]
    link_type = models.CharField(
        max_length=50, choices=link_type_choices, default="internal"
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

    def get_children(self):
        return self.children.filter(is_active=True)

    def has_children(self):
        return self.children.filter(is_active=True).exists()
