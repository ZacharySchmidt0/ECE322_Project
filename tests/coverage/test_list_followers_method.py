import unittest
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter, Choice

class TestListFollowersMethod(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test.db'
        self.tweeter = Tweeter(self.test_db)

    def tearDown(self):
        self.tweeter.conn.close()
        import os
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    @patch('InquirerPy.inquirer.select')
    @patch('builtins.print')
    @patch('time.sleep')
    def test_list_followers_with_followers(self, mock_sleep, mock_print, mock_select):
        # Mocking get_followers method to return a list of followers
        self.tweeter.get_followers = MagicMock(return_value=[(1, 'John Doe', 'john@example.com', 'City', 1.0, '2023-01-01')])
        mock_select.return_value.execute.return_value = 'x'

        self.tweeter.list_followers()

        # Verifying that inquirer.select was called with correct choices
        mock_select.assert_called_once()
        args, kwargs = mock_select.call_args
        self.assertIn(Choice(1, 'Name: John Doe, Email: john@example.com, City: City, Timezone: 1.0, Following Since: 2023-01-01'), args[0]['choices'])

    @patch('InquirerPy.inquirer.select')
    @patch('builtins.print')
    @patch('time.sleep')
    def test_list_followers_no_followers(self, mock_sleep, mock_print, mock_select):
        # Mocking get_followers method to return an empty list
        self.tweeter.get_followers = MagicMock(return_value=[])
        mock_select.return_value.execute.return_value = 'x'

        self.tweeter.list_followers()

        # Verifying that a message indicating no followers is printed
        mock_print.assert_called_with("You have no followers")
        mock_sleep.assert_called_once_with(1)

    @patch('InquirerPy.inquirer.select')
    def test_select_follower(self, mock_select):
        # Mocking get_followers method to return a list of followers
        self.tweeter.get_followers = MagicMock(return_value=[(1, 'John Doe', 'john@example.com', 'City', 1.0, '2023-01-01')])
        follower_id = 1
        mock_select.side_effect = [Choice(follower_id, "Follower Info"), Choice('x', "Return to Function Menu")]

        with patch.object(Tweeter, 'show_user_info') as mock_show_user_info:
            self.tweeter.list_followers()

            # Verifying that show_user_info is called for the selected follower
            mock_show_user_info.assert_called_once_with(follower_id, 'John Doe')

    @patch('InquirerPy.inquirer.select')
    def test_return_to_function_menu(self, mock_select):
        # Mocking get_followers method to return a list of followers
        self.tweeter.get_followers = MagicMock(return_value=[(1, 'John Doe', 'john@example.com', 'City', 1.0, '2023-01-01')])
        # Simulating the user choosing to return to the function menu
        mock_select.return_value.execute.return_value = 'x'

        with patch.object(Tweeter, 'function_menu') as mock_function_menu:
            self.tweeter.list_followers()

            # Verifying that the function_menu method is called when 'x' is selected
            mock_function_menu.assert_called_once()

if __name__ == '__main__':
    unittest.main()
