from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic.base import View

from .models import Post, Category


class PostList(View):
    """Список постов"""
    def get(self, request, slug=None):
        if slug is None:
            return render(request, 'news/posts-list.html', {'posts': Post.objects.all()})
        else:
            category_id = get_object_or_404(Category, slug=slug).id
            return render(request, 'news/posts-list.html', {'posts': Post.objects.filter(category_id=category_id)})


class PostDetail(View):
    """Один конкретный пост"""
    def get(self, request, slug):
        return render(request, 'news/post-detail.html', {'post': get_object_or_404(Post, slug=slug)})
