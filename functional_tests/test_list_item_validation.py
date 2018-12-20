from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    '''test item validation'''

    def test_cannot_add_empty_list_items(self):
        '''test: cannot add empty list items'''
        self.fail('write me!')
