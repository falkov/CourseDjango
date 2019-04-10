from django.db import models


class ContactFormModel(models.Model):
    """Модель формы обратной связи"""
    full_name = models.CharField('name', max_length=50)
    email = models.EmailField('email', max_length=50)
    text = models.TextField('сообщение')
    created = models.DateTimeField('дата и время сообщения', auto_now_add=True)

    def __str__(self):
        return r'{self.created} : {self.full_name} : {self.email}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-created']
