from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils import timezone
from phone_field import PhoneField

from taggit.managers import TaggableManager


class Post(models.Model):
    STATUS_CHOICE = [
        ('draft', "Draft"),
        ('published', "Published")
    ]
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, null=True)
    author = models.ForeignKey(User, related_name="blog_posts", on_delete=models.CASCADE)
    body = RichTextField()
    publish = models.DateField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default="draft")
    image_upload = models.ImageField(blank=True, null=True, upload_to="post_pics")

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail',
                       args=[self.publish.strftime('%Y'),
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])

    # For Tagging Features
    tags = TaggableManager()


# Model for Comments on a Post
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created', ]

    def __str__(self):
        return 'Comment By ' + f'{self.username} on {self.post.title} at {self.created}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default1.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} Profile Image"


def Profile_Create(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(Profile_Create, sender=User)


class LikeOrDislike(models.Model):
    post = models.ForeignKey(Post, related_name="like_dislike", on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
