from selenium import webdriver
from .base import FunctionalTest
from .list_page import ListPage
from .my_lists_page import MyListsPage


def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        print('do not quit')


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
        self.create_pre_authenticated_session("oni@example.com")

        self.browser = e_browser
        self.browser.get(self.live_server_url)
        list_page = ListPage(self).add_list_item('Get help')

        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute("placeholder"),
            "your-friend@example.com"
        )

        list_page.share_list_with('oni@example.com')

        self.browser = oni_browser
        MyListsPage(self).go_to_my_lists_page()

        self.browser.find_element_by_link_text('Get help').click()

        self.wait_for(lambda: self.assertEqual(
            list_page.get_list_owner(),
            'e@example.com'
        ))

        list_page.add_list_item('Hi Edith!')

        self.browser = e_browser
        self.browser.refresh()
        list_page.wait_for_row_in_list_table('Hi Edith!', 2)
