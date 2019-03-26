from django.db.models import Q
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.utils import timezone

from .models import Post, Category
from .forms import CommentForm


class PostList(ListView):
    """Список постов"""
    model = Post
    context_object_name = 'posts'
    template_name = 'news/short_post_list.html'

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')

        if category_slug is not None:
            qs = self.model.objects.filter(category__slug=category_slug)

            if qs.exists():
                self.paginate_by = qs.first().category.amount_for_pagination

                qs = qs.filter(
                    do_publish=True,
                    published_date__date__lte=timezone.now(),
                )

                if not self.request.user.is_authenticated:
                    qs = qs.filter(show_for_all=True)
        else:
            qs = self.model.objects.all()
            self.paginate_by = 8

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
    template_name = 'news/post_detail.html'

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
            return render(request, 'news/post_detail.html', {'post': get_object_or_404(Post, slug=slug), 'form': form})

        else:
            return HttpResponse(status=400)


class SearchForCategoryAndTitleList(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'news/short_post_list.html'
    paginate_by = 8

    def get_queryset(self):
        what_search = self.request.GET.get('search', '')
        qs = Post.objects.filter(Q(title__icontains=what_search) | Q(category__name__contains=what_search))
        return qs


class SearchForDateList(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'news/short_post_list.html'
    paginate_by = 8

    def get_queryset(self):
        days_amount = self.kwargs.get('days_amount')
        date_from = timezone.now() - timezone.timedelta(days=days_amount)
        qs = Post.objects.filter(published_date__gte=date_from)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchForDateList, self).get_context_data(**kwargs)
        days_amount = self.kwargs.get('days_amount')
        context['days_amount'] = days_amount if days_amount < 19_000 else 'за все время'
        context['date_from'] = timezone.now() - timezone.timedelta(days=days_amount)
        context['date_to'] = timezone.now()
        return context
