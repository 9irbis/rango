from django.test import TestCase
from rangoapp.models import Category
from django.core.urlresolvers import reverse


def add_test_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c


class CategoryModelTests(TestCase):

    def test_ensure_views_are_positive(self):
        cat = Category(name="nakul", views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0), True)

    def test_slug_line_creation(self):
        cat = Category(name = "Just another category")
        cat.save()
        self.assertEqual(cat.slug, "just-another-category")


class IndexViewTests(TestCase):

    def test_index_view_with_no_categories(self):
        response = self.client.get(reverse('rango_nspc:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories at present.")
        self.assertQuerysetEqual(response.context['categories'], [])

    def test_index_view_with_categories(self):
        add_test_cat('tmp', 1, 1)
        add_test_cat('temp', 0, 4)
        add_test_cat('tmp temp test', 1, 0)
        add_test_cat('test', 1, 2)
        response = self.client.get(reverse('rango_nspc:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'tmp temp test')
        self.assertEqual(len(response.context['categories']), 4)
