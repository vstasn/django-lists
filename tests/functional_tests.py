from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    '''test new user'''

    def setUp(self):
        '''install'''
        self.browser = webdriver.Firefox()

    def tearDown(self):
        '''uninstall'''
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')

        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish test')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
