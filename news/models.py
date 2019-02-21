from django.db import models


class Category(models.Model):
    """Модель категории"""
    name = models.CharField(verbose_name="Имя", max_length=50)
    slug = models.SlugField(verbose_name="url", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Tag(models.Model):
    """Модель тега"""
    name = models.CharField(verbose_name="Имя", max_length=50)
    slug = models.SlugField(verbose_name="url", max_length=100)

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

    def __str__(self):
        return f'title: {self.title}, text:{self.text}'

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-created"]


class Comment(models.Model):
    """Модель комментария"""
    text = models.TextField(verbose_name="Текст")
    post = models.ForeignKey(Post, verbose_name="Пост", on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)

    def __str__(self):
        return self.text[:50]  # комментарий м.б. очень большим

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
