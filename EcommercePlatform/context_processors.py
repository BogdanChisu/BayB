from category.models import Category
from product.models import Product


def get_all_categories(request):
    return {'all_categories': Category.objects.all()}


