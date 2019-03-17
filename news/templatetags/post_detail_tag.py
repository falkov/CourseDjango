from django import template

register = template.Library()


@register.inclusion_tag('news/base_tag.html')
def post_detail_tag(this_post, this_template='news/detail_post__template_default.html'):
    """Конкретный пост детально, шаблон зависит от категории, см. в admin"""
    return {
        'this_template': this_template,
        'this_post': this_post,
    }
