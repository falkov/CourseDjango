from django.shortcuts import render

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic.base import View

from .models import Post, Category, Comment


class PostList(View):
    def get(self, request):
        posts_all = Post.objects.all()  # все посты

        print('1 ----------')
        # Категория_1:
        #   Заголовок поста 9: Текст поста 9, теги: Тег_3, Тег_5, comments: Комментарий к посту 9: Каждый из
        #   Заголовок поста 5: Текст поста 5, теги: Тег_1, Тег_3, comments: Комментарий к посту 5: Предваритель
        # Категория_2:
        #   Заголовок поста 10: Текст поста 10, теги: Тег_1, Тег_5, comments: Комментарий к посту 10: А также
        #   Заголовок поста 6: Текст поста 6, теги: Тег_2, Тег_4, comments: Комментарий к посту 6: Внезапно, сд
        for category in Category.objects.all():
            print(f'{category.name}:')
            posts = Post.objects.filter(category_id=category.id)

            for post in posts:
                # ??? вопрос, как лучше:
                # так:      print(f'{post}'),  если в модели __str__= f'title: {self.title}, text:{self.text}'
                # или так:  print(f'{post.title}: {post.text}'),  если в модели обычный __str__

                this_tags = ''
                for tag in post.tags.all():
                    this_tags += tag.name + ', '

                this_comments = ''
                for comment in Comment.objects.filter(post_id=post.id):
                    this_comments += f'{comment.text[:50]} ... {comment.text[-50:]}, '

                print(f'  {post.title}: {post.text}, теги: {this_tags[:-2]}, comments: {this_comments[:-2]}')

        # все комментарии
        print('2 ----------')
        for comment in Comment.objects.all():
            reduce_comment = f'{comment.text[:50]} ... {comment.text[-50:]}'
            print(reduce_comment)

        # return HttpResponse(posts_all)
        return render(request, 'post-list.html', {
            'posts_all': posts_all,
            'comments_all': Comment.objects.all()
        })


class PostDetail(View):
    def get(self, request, post_number):
        # post = Post.objects.filter(id=post_number)
        post = get_object_or_404(Post, pk=post_number)
        comments = Comment.objects.filter(post_id=post_number)

        return render(request, 'post-detail.html', {
            'post': post,
            'comments': comments
        })
