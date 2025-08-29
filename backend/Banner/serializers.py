# serializers.py
from rest_framework import serializers
from .models import Banner

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = [
            'id',
            'title',
            'subtitle',
            'content',
            'image',
            'link',
            'display_order',
            'created_at',
        ]
