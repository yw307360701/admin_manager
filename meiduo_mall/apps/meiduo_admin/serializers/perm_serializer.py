from rest_framework import serializers
from django.contrib.auth.models import Permission, ContentType


class PermModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = [
            'id',
            'name',
            'codename',
            'content_type'
        ]


class ContenTypeSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = [
            'id',
            'name'
        ]