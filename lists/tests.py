from django.urls import resolve
from django.test import TestCase
from .views import home_page


class HomePageTest(TestCase):
    '''test home page'''

    def test_root_url_resolves_to_home_page_view(self):
        '''test: root url'''
        found = resolve('/')
        self.assertEqual(found.func, home_page)

