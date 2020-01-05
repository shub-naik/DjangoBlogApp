from django.utils.text import slugify
from rest_framework import serializers

# models importing
from ..models import Post


class PostBlogSerializer(serializers.ModelSerializer):
    # For Handling With the Foreign Key Data and Attributes.
    username = serializers.CharField(source="author.username")
    email = serializers.EmailField(source="author.email")

    class Meta:
        model = Post
        fields = ['title', 'body', 'username', 'email', 'created', 'updated', 'status', 'image_upload']


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'body', 'image_upload']


class PostDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'image_upload']


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'body', 'status', 'image_upload']
