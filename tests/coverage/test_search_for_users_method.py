import unittest
from unittest.mock import patch
from modules.Tweeter import Tweeter, Choice

class TestSearchForUsersMethod(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test.db'
        self.tweeter = Tweeter(self.test_db)

    def tearDown(self):
        self.tweeter.conn.close()
        import os
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    # Test for initial keyword input and no users found scenario
    @patch('InquirerPy.inquirer.text')
    @patch('builtins.print')
    @patch('time.sleep')
    def test_no_users_found(self, mock_sleep, mock_print, mock_text):
        mock_text.return_value.execute.return_value = 'nonexistent'
        with patch.object(Tweeter, 'search_for_user_query', return_value=[]), \
             patch.object(Tweeter, 'function_menu') as mock_function_menu:

            self.tweeter.search_for_users()

            mock_print.assert_called_with("No users found.")
            mock_function_menu.assert_called_once()

    # Test for handling next page ('n') option
    @patch('InquirerPy.inquirer.text')
    @patch('InquirerPy.inquirer.select')
    def test_next_page_option(self, mock_select, mock_text):
        mock_text.return_value.execute.return_value = 'keyword'
        mock_select.side_effect = [Choice('n', "Next Page"), Choice('x', "Return to Function Menu")]
        with patch.object(Tweeter, 'search_for_user_query', return_value=[(1, 'Name', 'Email', 'City', 1.0)]), \
             patch.object(Tweeter, 'function_menu') as mock_function_menu:

            self.tweeter.search_for_users()

            mock_function_menu.assert_called_once()
            # Verify that search_for_user_query is called twice for two pages
            self.assertEqual(Tweeter.search_for_user_query.call_count, 2)

    # Test for handling previous page ('p') option
    @patch('InquirerPy.inquirer.text')
    @patch('InquirerPy.inquirer.select')
    def test_previous_page_option(self, mock_select, mock_text):
        mock_text.return_value.execute.return_value = 'keyword'
        mock_select.side_effect = [Choice('n', "Next Page"), Choice('p', "Previous Page"), Choice('x', "Return to Function Menu")]
        with patch.object(Tweeter, 'search_for_user_query', return_value=[(1, 'Name', 'Email', 'City', 1.0)]), \
             patch.object(Tweeter, 'function_menu') as mock_function_menu:

            self.tweeter.search_for_users()

            mock_function_menu.assert_called_once()
            # Verify that search_for_user_query is called three times (two next page and one previous page)
            self.assertEqual(Tweeter.search_for_user_query.call_count, 3)

    # Test for handling user selection
    @patch('InquirerPy.inquirer.text')
    @patch('InquirerPy.inquirer.select')
    def test_user_selection(self, mock_select, mock_text):
        mock_text.return_value.execute.return_value = 'keyword'
        mock_select.return_value.execute.side_effect = ['1', 'x']
        with patch.object(Tweeter, 'search_for_user_query', return_value=[(1, 'Name', 'Email', 'City', 1.0)]), \
             patch.object(Tweeter, 'show_user_info') as mock_show_user_info, \
             patch.object(Tweeter, 'function_menu') as mock_function_menu:

            self.tweeter.search_for_users()

            mock_show_user_info.assert_called_once_with(1, 'Name')
            mock_function_menu.assert_called_once()

if __name__ == '__main__':
    unittest.main()
