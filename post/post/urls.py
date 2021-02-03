from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  url(r'^search/', include('blog.urls')),
                  url('admin/', admin.site.urls),
                  # url(r'^blog/', include('blog.urls')),
                  path('', include('blog.urls')),
                  # url(r'^search/', include('haystack.urls'))
                  path('api/blog/post/', include('blog.api.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
