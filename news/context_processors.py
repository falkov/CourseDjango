from .models import Category


def contextprocessor_categories_all(request):
    # return {'contextprocessor_categories_all': Category.objects.filter(parent__isnull=True)}
    return {'contextprocessor_categories_all': Category.objects.all()}
