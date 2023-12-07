import unittest
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter

class TestLogin(unittest.TestCase):

    def setUp(self):
        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.connection_patch = patch('modules.Tweeter.sqlite3.connect', return_value=self.mock_connection)
        self.connection_patch.start()

    def tearDown(self):
        self.connection_patch.stop()

    @patch('modules.Tweeter.inquirer.text')
    @patch('modules.Tweeter.inquirer.secret')
    @patch("modules.Tweeter.Tweeter.follow_feed")
    def test_login_success(self, mocked_follow_feed, mock_secret, mock_text):
        # Arrange: Mock user input for ID and password
        user_id = 'testuser'
        password = 'testpass'
        mock_text.return_value.execute.return_value = user_id
        mock_secret.return_value.execute.return_value = password

        # Mock the database response for a correct login
        self.mock_cursor.fetchone.return_value = (user_id,)
        def exit_program():
                return 1
        mocked_follow_feed.side_effect = exit_program
        
        tweeter_instance = Tweeter("test.db")
        tweeter_instance.login()
        self.assertIsNotNone(tweeter_instance.user_id)
        self.assertEqual(tweeter_instance.user_id, user_id)

    @patch('modules.Tweeter.inquirer.text')
    @patch('modules.Tweeter.inquirer.secret')
    @patch("modules.Tweeter.Tweeter.start_screen")
    def test_login_failure(self, mocked_start_screen, mock_secret, mock_text):
        # Arrange: Mock user input for ID and password
        user_id = 'testuser'
        password = 'wrongpass'
        mock_text.return_value.execute.return_value = user_id
        mock_secret.return_value.execute.return_value = password

        # Mock the database response for a failed login
        self.mock_cursor.fetchone.return_value = None
        def exit_program():
                return 1
        mocked_start_screen.side_effect = exit_program
        
        tweeter_instance = Tweeter("test.db")
        tweeter_instance.login()

        self.assertIsNone(tweeter_instance.user_id)

if __name__ == '__main__':
    unittest.main()
