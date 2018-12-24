import os
import poplib
import re
import time
from django.core import mail
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):
    '''test login system'''

    def wait_for_email(self, test_email, subject):
        '''wait for email'''
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        time.sleep(20)
        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('pop.yandex.ru')
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ['EMAIL_YA_PASSWORD'])
            while time.time() - start < 60:
                count, _ = inbox.stat()
                for i in range(1, 10):
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf8') for l in lines]
                    if f'Subject: {subject}' in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        except Exception as e:
            print(e)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()

    def test_can_get_email_link_to_log_in(self):
        '''test: can get email link to log in'''
        if self.staging_server:
            test_email = os.environ.get('EMAIL_YA_LOGIN')
        else:
            test_email = 'e@example.com'

        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(test_email)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # A message appears telling her an email has been sent
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element_by_tag_name('body').text
        ))

        body = self.wait_for_email(test_email, SUBJECT)

        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        self.browser.get(url)

        self.wait_to_be_logged_in(email=test_email)

        self.browser.find_element_by_link_text('Log out').click()

        self.wait_to_be_logged_out(email=test_email)
