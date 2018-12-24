from selenium import webdriver
from .base import FunctionalTest


def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass


class SharingTest(FunctionalTest):
    """sharing test"""

    def test_can_share_a_list_with_another_user(self):
        """test: can share a list with another user"""
        self.create_pre_authenticated_session("e@example.com")
        e_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(e_browser))

        oni_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(oni_browser))
        self.browser = oni_browser
        self.create_pre_authenticated_session("one@example.com")

        self.browser = e_browser
        self.browser.get(self.live_server_url)
        self.add_list_item("Get help")

        share_box = self.browser.find_element_by_css_selector('input[name="sharee"]')
        self.assertEqual(
            share_box.get_attribute("placeholder"), "your-friend@example.com"
        )
