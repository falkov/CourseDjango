# Generated by Django 2.1.7 on 2019-04-10 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactFormModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50, verbose_name='name')),
                ('email', models.EmailField(max_length=50, verbose_name='email')),
                ('text', models.TextField(verbose_name='сообщение')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='дата и время сообщения')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
                'ordering': ['-created'],
            },
        ),
    ]