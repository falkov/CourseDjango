# Generated by Django 2.1.7 on 2019-03-12 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20190310_1042'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='amount_for_pagination',
            field=models.PositiveIntegerField(default=20, verbose_name='Кол. для пагинации'),
        ),
        migrations.AddField(
            model_name='category',
            name='template',
            field=models.CharField(default='category_posts_template_default.html', max_length=100, verbose_name='Используемый шаблон'),
        ),
    ]
