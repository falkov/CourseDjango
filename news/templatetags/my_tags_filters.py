from django import template

from news.models import Post, Category

register = template.Library()


@register.inclusion_tag('my_tags_filters/my_tag__categories_list.html')
def my_tag__categories_list():
    """Список всех категорий"""
    return {'from_my_tag__categories_list': Category.objects.all()}


@register.inclusion_tag('my_tags_filters/my_tag__post_short.html')
def my_tag__post_short(this_post):
    """Конкретный пост кратко"""
    return {'from_my_tag__posts_short': this_post}


@register.inclusion_tag('my_tags_filters/my_tag__post_detail.html')
def my_tag__post_detail(this_post):
    """Конкретный пост детально"""
    return {'from_my_tag__posts_detail': this_post}
