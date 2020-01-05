from django.http import JsonResponse
from django.utils.text import slugify
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, RetrieveDestroyAPIView, CreateAPIView, \
    RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import PostBlogSerializer, PostUpdateSerializer, PostDeleteSerializer, PostCreateSerializer
from ..models import Post


class PostCreateApiView(CreateAPIView):
    serializer_class = PostCreateSerializer

    def perform_create(self, serializer):
        slug_field = slugify(self.request.data['title'])
        print(slug_field)
        serializer.save(author=self.request.user, slug=slug_field)


class PostListApiView(ListAPIView):
    # queryset = Post.objects.all()
    serializer_class = PostBlogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(status__icontains="Published")


class PostDetailApiView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostBlogSerializer
    lookup_field = "slug"


class PostUpdateView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateSerializer
    lookup_field = "pk"


class PostDeleteView(RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDeleteSerializer
    lookup_field = "slug"
