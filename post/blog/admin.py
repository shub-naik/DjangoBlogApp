from django.contrib import admin
from .models import Post, Comment, Profile, LikeOrDislike


# This is Used For Customising the Admin Look of the Models
# Hence, we Create the class whose name can be anything but then we have to pass that name in the admin.register.site() function

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish', 'created', 'updated', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['publish', 'status']

admin.site.register(Post,PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'post', 'created']
    search_fields = ['username', 'email', 'body']
    list_filter = ['created', 'updated']

admin.site.register(Comment, CommentAdmin)


class ProfileImages(admin.ModelAdmin):
    list_display = ['user', 'image']


admin.site.register(Profile, ProfileImages)

class LikeDislikeAdminModel(admin.ModelAdmin):
    list_display = ['username','post','like','dislike']

admin.site.register(LikeOrDislike, LikeDislikeAdminModel)

