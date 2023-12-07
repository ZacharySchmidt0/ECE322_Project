import unittest
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter

class TestShowUserInfo(unittest.TestCase):
    def setUp(self):
        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.connection_patch = patch('modules.Tweeter.sqlite3.connect', return_value=self.mock_connection)
        self.connection_patch.start()

        self.tweeter_instance = Tweeter("test.db")
        self.tweeter_instance.user_id = 1  # Mocking a logged-in user with user_id 1

    def tearDown(self):
        self.connection_patch.stop()

    @patch('modules.Tweeter.inquirer.select')
    def test_show_user_info_until_loop(self, mock_select):
        # Arrange
        user_id = 2
        user_name = "User2"
        user_info = (user_id, user_name, "user2@example.com", "City2", 2.0)
        self.mock_cursor.fetchone.return_value = user_info

        fake_tweets = [
            (10, "Tweet text 1", "2023-01-01"),
            (11, "Tweet text 2", "2023-01-02")
        ]
        self.mock_cursor.fetchall.return_value = fake_tweets

        # Mock user interactions to exit at the first prompt in the while loop
        mock_select.return_value.execute.return_value = 'x'

        # Act
        self.tweeter_instance.show_user_info(user_id, user_name)

        # Assert
        # Check that the SQL queries were executed correctly
        self.mock_cursor.execute.assert_any_call(
            'SELECT COUNT(*) FROM tweets WHERE writer = ?;', (user_id,)
        )
        self.mock_cursor.execute.assert_any_call(
            "SELECT COUNT(*) FROM follows WHERE flwer = ?;", (user_id,)
        )

        # Check that inquirer.select was called to handle the user interaction
        mock_select.assert_called_once()

if __name__ == '__main__':
    unittest.main()
