from django.test import TestCase
from django.contrib import auth
from accounts.models import Token

User = auth.get_user_model()


class UserModelTest(TestCase):
    '''test user model'''

    def test_user_is_valid_with_email_only(self):
        '''test: user is valid with email only'''
        user = User(email='a@b.com')
        user.full_clean()

    def test_email_is_primary_key(self):
        '''test: email is primary key'''
        user = User(email='a@b.com')
        self.assertEqual(user.pk, 'a@b.com')

    def test_no_problem_with_auth_login(self):
        '''test: no problem with auth login'''
        user = User.objects.create(email='e@example.com')
        user.backend = ''
        request = self.client.request().wsgi_request
        auth.login(request, user)


class TokenModelTest(TestCase):
    '''test token model'''

    def test_links_user_with_auto_generated_uid(self):
        '''test: links user with auto generated uid'''
        token1 = Token.objects.create(email='a@b.com')
        token2 = Token.objects.create(email='a@b.com')
        self.assertNotEqual(token1.uid, token2.uid)
