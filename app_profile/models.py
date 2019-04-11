from django.contrib.auth.models import User
from django.db import models


def get_userprofile_avatar(instance, filename):
    return f'{instance.user.id}/{filename}'


class UserProfile(models.Model):
    """Модель профиля пользователя"""
    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    avatar = models.ImageField('Аватар', upload_to=get_userprofile_avatar, blank=True, null=True)
    age = models.PositiveIntegerField('Возраст')


    def __str__(self):
        return r'{self.user} : {self.age}'

    class Meta:
        verbose_name = 'Дополнительный профиль пользователя'
        verbose_name_plural = 'Дополнительные профили пользователей'
        ordering = ['user']
