from django.test import TestCase
from unittest.mock import patch, call
from accounts.models import Token


class SendLoginEmailViewTest(TestCase):
    '''test view, which send email for log in'''

    def test_redirects_to_home_page(self):
        '''test: redirects to home page'''
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'edit@example.com'
        })
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        '''test: sends mail to address from post'''
        self.client.post('/accounts/send_login_email', data={
            'email': 'e@example.com'
        })

        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, 'noreply@superlists')
        self.assertEqual(to_list, ['e@example.com'])

    def test_adds_success_message(self):
        '''test: adds success message'''
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'e@example.com'
        }, follow=True)

        message = list(response.context['messages'])[0]
        self.assertEqual(
            message.message,
            "Check your email, we've sent you a link you can use to log in."
        )
        self.assertEqual(message.tags, 'success')

    @patch('accounts.views.messages')
    def test_adds_success_message_with_mocks(self, mock_messages):
        '''test: adds success message with mock'''
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'e@example.com'
        })

        expected = "Check your email, we've sent you a link you can use to log in."
        self.assertEqual(
            mock_messages.success.call_args,
            call(response.wsgi_request, expected),
        )

    def test_creates_token_associated_with_email(self):
        '''test: creates token associated with email'''
        self.client.post('/accounts/send_login_email', data={
            'email': 'e@example.com'
        })
        token = Token.objects.first()
        self.assertEqual(token.email, 'e@example.com')

    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        '''test: sends link to login using token uid'''
        self.client.post('/accounts/send_login_email', data={
            'email': 'e@example.com'
        })

        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)


@patch('accounts.views.auth')
class LoginViewTest(TestCase):
    '''login view test'''

    def test_redirects_to_home_page(self, mock_auth):
        '''test: redirects to home page'''
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertRedirects(response, '/')

    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        '''test: calls authenticate with uid from get request'''
        self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(uid='abcd123')
        )

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        '''test: calls auth login with user if there is one'''
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )

    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
        '''test: does not login if user is not authenticated'''
        mock_auth.authenticate.return_value = None
        self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(mock_auth.login.called, False)
