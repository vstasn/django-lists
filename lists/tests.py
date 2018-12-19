from django.test import TestCase


class HomePageTest(TestCase):
    '''test home page'''

    def test_uses_home_template(self):
        '''test: home page return html'''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
