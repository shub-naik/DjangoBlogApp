from django.conf.urls import url

from .views import PostListApiView, PostDetailApiView, PostUpdateView, PostDeleteView, PostCreateApiView

urlpatterns = [
    # Retrieve Single Post By Slug Field
    url(r'^PostDetail/(?P<slug>[-\w]+)/$', PostDetailApiView.as_view(), name="PostDetailApi"),

    # Retrieve All Posts
    url(r'^$', PostListApiView.as_view(), name="PostListApi"),

    # Create New Post
    url(r'^create/$', PostCreateApiView.as_view(), name="PostCreateApi"),

    # Update Already Created Post
    url(r'^update_post/(?P<pk>[0-9]+)/$', PostUpdateView.as_view(), name='update_post_api'),

    # Delete Already Created Post by Id
    url(r'^delete_post/(?P<slug>[-\w]+)/$', PostDeleteView.as_view(), name='delete_post_api'),
]
