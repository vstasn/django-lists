from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    '''test layout and styling'''

    def test_layout_and_styling(self):
        '''test layout and styling'''
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(900, 768)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            450,
            delta=10
        )