# python function which takes request as an argument and returns a dictionary of data as a context

from category.models import CategoryModel


def menu_links(request):
    links = CategoryModel.objects.all() # get all categories from model
    return dict(links=links)