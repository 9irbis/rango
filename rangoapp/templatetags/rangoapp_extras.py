from django import template
from rangoapp.models import Category

register = template.Library()


@register.inclusion_tag('rangoapp/all_cats.html')
def get_all_categories(active_cat=None):
    return {'all_cats': Category.objects.all(), 'act_cat': active_cat}
