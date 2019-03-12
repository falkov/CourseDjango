from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, HttpResponse
from django.views.generic import ListView
from django.views.generic.base import View
import datetime

from .models import Post, Category
from .forms import CommentForm


# class PostList(View):
#     """Список постов"""
#     def get(self, request, slug=None):
#         if slug is None:
#             return render(request, 'news/posts-list.html', {'posts': Post.objects.all()})
#         else:
#             category_id = get_object_or_404(Category, slug=slug).id
#             return render(request, 'news/posts-list.html', {'posts': Post.objects.filter(category_id=category_id)})


class PostList(ListView):
    """Список постов"""
    model = Post
    context_object_name = 'posts'
    template_name = 'news/posts-list.html'

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')

        if category_slug is None:
            self.paginate_by = 20
            qs = self.model.objects.all()
        else:
            self.paginate_by = get_object_or_404(Category, slug=self.kwargs.get('slug')).amount_for_pagination

            category_id = get_object_or_404(Category, slug=self.kwargs.get('slug')).id
            qs = self.model.objects.filter(category_id=category_id)

        qs = qs.filter(do_publish=True)                                 # отмечены к публикации
        qs = qs.filter(published__date__lte=datetime.datetime.today())  # дата публикации не превышает текущую дату
        qs = qs.filter(show_for_all=True)                               # показывать для всех

        return qs


class PostDetail(View):
    """Один конкретный пост"""

    def get(self, request, slug):
        form = CommentForm()
        return render(request, 'news/post-detail.html', {'post': get_object_or_404(Post, slug=slug), 'form': form})

    def post(self, request, slug):
        form = CommentForm(request.POST)

        if form.is_valid():
            # my_text = form.cleaned_data['text']
            form = form.save(commit=False)
            form.post = Post.objects.get(slug=slug)
            form.save()

            # возврат на тот-же пост с только что добавленным комментом
            form = CommentForm()
            return render(request, 'news/post-detail.html', {'post': get_object_or_404(Post, slug=slug), 'form': form})

        else:
            return HttpResponse(status=400)
