from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField  # optional, if you want rich text for banner content

class Banner(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    content = RichTextField(blank=True, null=True)  # optional detailed content
    image = models.ImageField(upload_to="banners/")  # banner image
    link = models.URLField(blank=True, null=True)  # optional link when banner is clicked
    is_active = models.BooleanField(default=True)  # control visibility
    display_order = models.PositiveIntegerField(default=0)  # for ordering banners
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return self.title
