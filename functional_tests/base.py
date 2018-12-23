import os
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from .server_tools import reset_database

MAX_WAIT = 10


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):
    '''functional test'''

    def setUp(self):
        '''install'''
        self.browser = webdriver.Firefox()
        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server:
            self.live_server_url = 'http://' + self.staging_server
            reset_database(self.staging_server)

    def tearDown(self):
        '''uninstall'''
        self.browser.quit()

    @wait
    def wait_for_row_in_list_table(self, row_text):
        '''wait a row in list table'''
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    @wait
    def wait_for(self, fn):
        '''wait'''
        return fn()

    def get_item_input_box(self):
        '''get input box for item'''
        return self.browser.find_element_by_id('id_text')

    @wait
    def wait_to_be_logged_in(self, email):
        '''wait to be logged in'''
        self.browser.find_element_by_link_text('Log out')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        '''wait to be logged out'''
        self.wait_for(
            lambda: self.browser.find_element_by_name('email')
        )
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)
