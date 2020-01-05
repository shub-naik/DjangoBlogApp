from sys import path

from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list'),
    url(r'^$', views.post_list, name='post_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', views.post_detail,
        name='post_detail'),
    url(r'^(?P<post_id>\d+)/share/$', views.PostShare, name='share'),
    url(r'^search/', views.search_titles, name='search'),

    # login url
    # url(r'login/', views.login_view, name="login")
    url(r'^login/$', auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name="registration/logout.html"),
        name="logout"),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^register/$', views.register, name='register'),

    # like and dislike urls
    url(r'^like_dislike/$',views.like_dislike,name='like_dislike'),

    # create posts url
    url(r'^create_post/', views.PostCreateView.as_view(), name="create_post"),

    # update posts url
    url(r'^update_post/(?P<pk>[0-9]+)/$', views.PostUpdateView.as_view(), name='update_post'),

    # delete posts url
    url(r'^delete_post/(?P<pk>[0-9]+)/post/$', views.PostDeleteView.as_view(template_name="blog/post/post_confirm_delete.html"), name='delete_post'),
]
