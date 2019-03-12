import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Category(models.Model):
    """Модель категории"""
    name = models.CharField(verbose_name="Имя", max_length=50)
    slug = models.SlugField(verbose_name="slug", max_length=100)
    amount_for_pagination = models.PositiveIntegerField(verbose_name='Кол. для пагинации', default=20)
    template = models.CharField(verbose_name='Используемый шаблон', max_length=100, blank=False,
                                default='category_posts_template_default.html')

    def __str__(self):
        return self.name

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
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    edited = models.DateTimeField(verbose_name="Дата редактирования", blank=False, default=timezone.now)
    published = models.DateTimeField(verbose_name="Дата публикации", blank=False, default=timezone.now)
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

    def created_short(self):
        return self.created.strftime("%d.%m.%Y")

    def edited_short(self):
        return self.edited.strftime("%d.%m.%Y")

    def published_short(self):
        return self.published.strftime("%d.%m.%Y")

    def get_comments(self):
        return Comment.objects.filter(post=self.id)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-created"]


class Comment(models.Model):
    """Модель комментария"""
    text = models.TextField(verbose_name="Текст")
    post = models.ForeignKey(Post, verbose_name="Пост", on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    moderation = models.BooleanField("Разрешено к публикации", default=False)

    def __str__(self):
        return self.post.title

    def text_short(self):
        return self.text[:25]

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
