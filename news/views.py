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


class Search(View):
    def get(self, request):
        search = request.GET.get('search', None)

        # context = Post.objects.filter(title__icontains=search) | Post.objects.filter(category__name__contains=search)
        context = Post.objects.filter(Q(title__icontains=search) | Q(category__name__contains=search))

        return render(request, 'news/short_post_list.html', {'posts': context})


class SearchForDate(View):
    def get(self, request, days_amount):
        date_from = timezone.now() - timezone.timedelta(days=days_amount)
        date_to = timezone.now()  # если нужно будет искать за два месяца назад (например); пока datetime.now()
        context = Post.objects.filter(published_date__gte=date_from)

        return render(request, 'news/short_post_list.html', {
            'posts': context,
            'days_amount': days_amount if days_amount < 19_000 else 'за все время',
            'date_from': date_from,
            'date_to': date_to,
        })
