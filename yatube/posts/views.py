from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.models import User

from .models import Group, Post
from .forms import PostForm

COUNTER_POSTS = 10


def index(request):
    # posts = Post.objects.all()[:COUNTER_POSTS]
    post_list = Post.objects.all()
    paginator = Paginator(post_list, COUNTER_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Главная страница Yatube',
        # 'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    teamplate = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    # posts = group.group.all()[:COUNTER_POSTS]
    post_list = group.group.all()
    paginator = Paginator(post_list, COUNTER_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': group.title,
        'group': group,
        # 'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, teamplate, context)


def profile(request, username):
    teamplate = 'posts/profile.html'
    user_profile = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author__username=username).all()
    post_count = post_list.count()
    paginator = Paginator(post_list, COUNTER_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'user_profile': user_profile,
        'username': username,
        'title': f'Профайл пользователя {username}',
        'page_obj': page_obj,
        'post_count': post_count,
    }
    return render(request, teamplate, context)


def post_detail(request, post_id):
    teamplate = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    post_count = Post.objects.filter(author=post.author).count()
    post_text = post.text[:30]
    context = {
        'title': f'Пост {post_text}',
        'post': post,
        'post_count': post_count,
    }
    return render(request, teamplate, context)


@login_required
def post_create(request):
    teamplate = 'posts/create_post.html'
    form = PostForm(request.POST or None)
    context = {
        'form': form,
        'title': 'Новый пост',
    }
    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', post.author)
    return render(request, teamplate, context)


@login_required
def post_edit(request, post_id):
    teamplate = 'posts/create_post.html'
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST or None, instance=post)
    context = {
        'form': form,
        'title': 'Редактировать пост',
        'is_edit': True,
        'post': post,
    }
    if post.author == request.user:
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('posts:post_edit', post.author)
        form = PostForm(instance=post)
        return render(request, teamplate, context)
    return redirect('posts:post_edit')
