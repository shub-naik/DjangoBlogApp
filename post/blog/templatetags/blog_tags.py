from django.db.models import Count

from ..models import Post

from django import template

register=template.Library()

@register.inclusion_tag('blog/post/latest_post.html')
def show_latest_posts(count=5):
    latest_post=Post.objects.filter(status="published").order_by("-publish")[:count]
    return {"latest_post":latest_post}

@register.simple_tag
def get_most_commented(count=5):
    return Post.objects.filter(status="published").annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]