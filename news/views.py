from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from datetime import datetime

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

        if category_slug is not None:
            qs = self.model.objects.filter(category__slug=category_slug)

            if qs.exists():
                self.paginate_by = qs.first().category.amount_for_pagination

                qs = qs.filter(
                    do_publish=True,
                    published_date__date__lte=datetime.now(),
                )

                if not self.request.user.is_authenticated:
                    qs = qs.filter(show_for_all=True)
        else:
            qs = self.model.objects.all()
            self.paginate_by = 20

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        category_slug = self.kwargs.get('slug')

        if category_slug is None:
            context['what_category'] = 'Все категории'
        else:
            context['what_category'] = Category.objects.filter(slug=category_slug).first().name

        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news/post-detail.html'

    # def get_queryset(self):
    #     post = Post.objects.get(
    #         category__slug=self.kwargs.get('slug'),
    #         do_publish=True,
    #         published_date__lte=datetime.now(),
    #     )
    #     return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm
        return context

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
