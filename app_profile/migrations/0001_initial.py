# Generated by Django 2.1.7 on 2019-04-11 16:02

import app_profile.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=app_profile.models.get_userprofile_avatar, verbose_name='Аватар')),
                ('age', models.PositiveIntegerField(verbose_name='Возраст')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Дополнительный профиль пользователя',
                'verbose_name_plural': 'Дополнительные профили пользователей',
                'ordering': ['user'],
            },
        ),
    ]
