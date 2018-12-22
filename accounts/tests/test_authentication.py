from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token

User = get_user_model()


class AuthenticationTest(TestCase):
    '''test authentication'''

    def test_returns_None_if_no_such_token(self):
        '''test: returns None if no such token'''
        result = PasswordlessAuthenticationBackend().authenticate(
            None,
            uid='no-such-token'
        )
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        '''test: returns new user with correct email if token exists'''
        email = 'e@example.com'
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(
            None,
            uid=token.uid
        )
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        '''test: returns existing user with correct email if token exists'''
        email = 'e@example.com'
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(
            None,
            uid=token.uid
        )
        self.assertEqual(user, existing_user)


class GetUserTest(TestCase):
    '''test get user'''

    def test_gets_user_by_email(self):
        '''test: gets user by email'''
        User.objects.create(email='ant@example.com')
        desired_user = User.objects.create(email='e@example.com')
        found_user = PasswordlessAuthenticationBackend().get_user(
            'e@example.com'
        )
        self.assertEqual(found_user, desired_user)

    def test_returns_None_if_no_user_with_that_email(self):
        '''test: returns None if no user with that email'''
        self.assertIsNone(
            PasswordlessAuthenticationBackend().get_user('e@example.com')
        )
