from category.models import Category


def get_all_categories(request):
    return {'all_categories': Category.objects.all()}