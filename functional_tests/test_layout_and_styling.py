from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    '''test layout and styling'''

    def test_layout_and_styling(self):
        '''test layout and styling'''
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(900, 768)

        self.add_list_item('testing')
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            450,
            delta=10
        )
