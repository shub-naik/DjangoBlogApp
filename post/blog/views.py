from django.db.models.signals import post_save, pre_save
from django.db.transaction import commit
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template.context_processors import csrf
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.utils.decorators import method_decorator
from haystack.query import SearchQuerySet

# Models Import Appears Here
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

# Custom Forms
from .forms import EmailPostForm, CommentForm, LoginForm, RegisterForm, UserUpdateForm, ProfileUpdateForm

from .models import Post, LikeOrDislike

# importing models for taggit features
from taggit.models import Tag


# For All Posts Display
def post_list(request, tag_slug=None):
    posts = Post.objects.filter(status='published')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {}
    context.update(csrf(request))
    context['tag'] = tag
    context['posts'] = posts
    context['page'] = page
    # context = {'posts': posts, 'page': page, 'tag': tag}
    return render(request, 'blog/post/list.html', context)


# Post List Using Class Based Views
class PostListView(ListView):
    queryset = Post.objects.filter(status='published')
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


# For Single Post Display
@login_required
def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post,
                             slug=slug,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             status="published"
                             )
    comments = post.comments.all()

    # Similar Posts To This Post By Tags.
    post_tags_id = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(status="published").filter(tags__in=post_tags_id).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('title')).order_by('-same_tags', "-publish")[:5]

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = CommentForm(instance=request.user)
    context = {'post': post, 'comments': comments, 'comment_form': comment_form, 'similar_posts': similar_posts}
    return render(request, 'blog/post/detail.html', context)


# Sending Post By Mail
@login_required
def PostShare(request, post_id):
    sent = False
    post = get_object_or_404(Post, id=post_id, status__icontains='published')
    if request.method == 'POST':
        form = EmailPostForm(request.POST, initial={'email': "naikshub8412@gmail.com", 'name': post.author})
        if form.is_valid():
            cleaned_data = form.cleaned_data
            subject = f'Message From {cleaned_data["name"]} to {cleaned_data["email"]} and Title of the Post is {post.title}'
            message = f'Message is {post.body} and Comments are {cleaned_data["comments"]}'
            send_mail(subject, message, 'naikshub8412@gmail.com', [cleaned_data['to']], fail_silently=False)
            sent = True
    else:
        form = EmailPostForm(initial={'email': "naikshub8412@gmail.com", 'name': post.author})
    context = {'post': post, 'form': form, 'sent': sent}
    return render(request, 'blog/post/share.html', context)


# for search features.
def search_titles(request):
    if request.method == "GET":
        request_string = request.GET.get('search_text')
        if request_string == "":
            return render(request, 'blog/post/ajax_search.html', {'posts': ""})
    # else:
    #     request_string = ''
    # posts=SearchQuerySet().autocomplete(content_auto=request.POST.get('search_text',''))
    posts = Post.objects.filter(title__icontains=request_string)
    return render(request, 'blog/post/ajax_search.html', {'posts': posts})


# login view
# def login_view(request):
#     if request.method == "POST":
#         loginform = LoginForm(data=request.POST)
#         if loginform.is_valid():
#             cd = loginform.cleaned_data
#             user = authenticate(username=cd['username'], password=cd['password'])
#             if user is not None:
#                 login(request, user)
#                 return HttpResponse("Login SuccessFully !!!")
#             else:
#                 return HttpResponse("UnSuccessFully Login !!!")
#     else:
#         loginform = LoginForm()
#     return render(request, "blog/post/login.html", {"loginform": loginform})

def register(request):
    if request.method == "POST":
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {"form": form})


@login_required
def profile(request):
    your_posted_posts = Post.objects.filter(status="published")[:6]
    if request.method == "POST":
        user_form = UserUpdateForm(data=request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,
                                         request.FILES,
                                         instance=request.user.profile,
                                         )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {'user_form': user_form, 'profile_form': profile_form, "posts": your_posted_posts}
    return render(request, 'registration/profile.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'body', 'status', 'tags', 'image_upload']

    # def get_success_url(self, **kwargs):
    #     return self.object.get_absolute_url()

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    #     # return super(PostCreateView, self).form_valid(form)


# def AfterPostPosting(sender, instance, created, **kwargs):
#     if created:
#         InstanceClass = instance.__class__
#         instance_slug = slugify(instance.title)
#         same_slug_list_exists = InstanceClass.objects.filter(slug=instance_slug).exclude(id=instance.id)
#         if same_slug_list_exists:
#             instance_slug = slugify(instance.title) + "-" + str(instance.id)
#         else:
#             instance_slug = slugify(instance.title)
#         instance.slug = instance_slug
#         instance.save()
# 
# 
# post_save.connect(AfterPostPosting, sender=Post)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'body', 'status', 'tags', 'image_upload']
    template_name = "blog/post_update.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()  # This will return the post which we are going to update
        if post.author == self.request.user:
            return True
        return False


# post_save signal after the update post request is done.
def AfterPostUpdate(sender, instance, created, **kwargs):
    queryset = Post.objects.filter(slug=instance.slug).update(slug=instance.title)
    HttpResponseRedirect(reverse_lazy("post_detail", args=[instance.publish.strftime('%Y'),
                                                           instance.publish.strftime('%m'),
                                                           instance.publish.strftime('%d'),
                                                           slugify(instance.title)]))


post_save.connect(AfterPostUpdate, sender=Post)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("post_list")

    def test_func(self):
        post = self.get_object()  # This will return the post which we are going to update
        if post.author == self.request.user:
            return True
        return False


# Like and Dislike Views
@login_required
def like_dislike(request):
    if request.method == "GET":
        like_id = request.GET.get('like_id')
        dislike_id = request.GET.get('dislike_id')

        if like_id is not None:
            post_liked = Post.objects.get(id=like_id)
            post_liked_object = LikeOrDislike.objects.filter(username=request.user.username, post=post_liked)
            post_object_exists = post_liked_object.exists()
            if not post_object_exists:
                LikeOrDislike.objects.create(username=request.user.username, post=post_liked, like=1,
                                             dislike=0)
            else:
                post_liked_object = post_liked_object[0]
                if post_liked_object.like == 1:
                    post_liked_object.like = 0
                elif post_liked_object.like == 0:
                    post_liked_object.like = 1
                post_liked_object.dislike = 0
                post_liked_object.save()
        else:
            post_disliked = Post.objects.get(id=dislike_id)
            post_disliked_object = LikeOrDislike.objects.filter(username=request.user.username, post=post_disliked)
            post_disliked_object_exists = post_disliked_object.exists()
            if not post_disliked_object_exists:
                LikeOrDislike.objects.create(username=request.user.username, post=post_disliked, like=0,
                                             dislike=1)
            else:
                post_disliked_object = post_disliked_object[0]
                post_disliked_object.like = 0
                if post_disliked_object.dislike == 1:
                    post_disliked_object.dislike = 0
                elif post_disliked_object.dislike == 0:
                    post_disliked_object.dislike = 1
                post_disliked_object.save()
        return HttpResponse("hello")
