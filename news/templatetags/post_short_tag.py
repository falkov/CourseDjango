from django import template

register = template.Library()


@register.inclusion_tag('news/base_tag.html')
def post_short_tag(this_post, this_template='news/short_post__template_default.html'):
    """Конкретный пост кратко, шаблон зависит от категории, см. в admin"""
    return {
        'this_template': this_template,
        'this_post': this_post,
    }
