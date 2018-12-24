from .base import FunctionalTest


class MyListsTest(FunctionalTest):
    '''test app "my lists"'''

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        '''test: logged in users lists are saved as my lists'''
        self.create_pre_authenticated_session('e@example.com')

        self.browser.get(self.live_server_url)
        self.add_list_item('Reticulate splines')
        self.add_list_item('Immanentize eschaton')
        first_list_url = self.browser.current_url

        self.browser.find_element_by_link_text('My lists').click()

        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Reticulate splines')
        )
        self.browser.find_element_by_link_text('Reticulate splines').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        self.browser.get(self.live_server_url)
        self.add_list_item('Click cows')
        second_list_url = self.browser.current_url

        self.browser.find_element_by_link_text('My lists').click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Click cows')
        )
        self.browser.find_element_by_link_text('Click cows').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_link_text('My lists'),
            []
        ))
