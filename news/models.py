from django.db import models


class Category(models.Model):
    """Модель категории"""
    name = models.CharField(verbose_name="Имя", max_length=50)
    slug = models.SlugField(verbose_name="slug", max_length=100)

    def __str__(self):
        return self.name

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
    title = models.CharField(verbose_name="Заголовок", max_length=100)
    text = models.TextField(verbose_name="Текст")
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, verbose_name="Теги")
    slug = models.SlugField(verbose_name="slug", max_length=100, default="")

    def __str__(self):
        return f'title: {self.title}, text:{self.text}'

    def text_short(self):
        return self.text[:25]

    def title_short(self):
        return self.title[:25]

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
