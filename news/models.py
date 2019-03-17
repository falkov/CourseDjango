import datetime

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """Модель категории"""
    name = models.CharField(verbose_name="Имя", max_length=50)
    slug = models.SlugField(verbose_name="slug", max_length=100)
    amount_for_pagination = models.PositiveIntegerField(verbose_name='Кол. для пагинации', default=20)

    short_post_template = models.CharField(verbose_name='Шаблон для постов short', max_length=100, blank=False,
                                           default='news/short_post__template_default.html')

    detail_post_template = models.CharField(verbose_name='Шаблон для постов detail', max_length=100, blank=False,
                                            default='news/detail_post__template_default.html')

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    # class MPTTMeta:
    #     order_insertion_by = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_posts_list', kwargs={'slug': self.slug})

    def pagination_amount(self):
        return self.amount_for_pagination

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Tag(models.Model):
    """Модель тега"""
    name = models.CharField(verbose_name="Имя", max_length=50)
    slug = models.SlugField(verbose_name="slug", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Post(models.Model):
    """Модель поста"""
    DO_PUBLISH_CHOICES = (
        (True, 'Да'),
        (False, 'Нет'),
    )

    SHOW_POST_CHOICES = (
        (True, 'Для всех'),
        (False, 'Только для зарегистрированных'),
    )

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(verbose_name="Заголовок", max_length=100)
    subtitle = models.CharField(verbose_name='Подзаголовок', max_length=100, blank=False, default='')
    text = models.TextField(verbose_name="Текст")
    created_date = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    edited_date = models.DateTimeField(verbose_name="Дата редактирования", blank=False, default=timezone.now)
    published_date = models.DateTimeField(verbose_name="Дата публикации", blank=False, default=timezone.now)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, verbose_name="Теги")
    slug = models.SlugField(verbose_name="slug", max_length=100, blank=False, default="")
    image_main = models.ImageField(verbose_name='Главное изображение', blank=True)
    do_publish = models.BooleanField(verbose_name='Опубликовать', choices=DO_PUBLISH_CHOICES, blank=False, default=True)
    show_for_all = models.BooleanField(verbose_name='Показывать для всех', choices=SHOW_POST_CHOICES, blank=False,
                                       default=True)
    template = models.CharField(verbose_name='Используемый шаблон', max_length=100, blank=False,
                                default='post_template_default.html')

    def __str__(self):
        return f'title: {self.title}, text:{self.text}'

    def text_short(self):
        return self.text[:25]

    def title_short(self):
        return self.title[:25]

    def created_date_short(self):
        return self.created_date.strftime("%d.%m.%Y")

    def edited_date_short(self):
        return self.edited_date.strftime("%d.%m.%Y")

    def published_date_short(self):
        return self.published_date.strftime("%d.%m.%Y")

    def get_comments(self):
        return Comment.objects.filter(post=self.id)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-created_date"]


class Comment(MPTTModel):
    """Модель комментария"""
    text = models.TextField(verbose_name="Текст")
    post = models.ForeignKey(Post, verbose_name="Пост", on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    moderation = models.BooleanField("Разрешено к публикации", default=False)

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.post.title

    def text_short(self):
        return self.text[:25]

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
