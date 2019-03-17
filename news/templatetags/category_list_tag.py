from django import template
from news.models import Category

register = template.Library()


@register.inclusion_tag('news/category_list.html')
def category_list_tag():
    return {'category_list': Category.objects.all()}
