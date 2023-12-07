import unittest
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter

class TestLogout(unittest.TestCase):
    def setUp(self):
        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.connection_patch = patch('modules.Tweeter.sqlite3.connect', return_value=self.mock_connection)
        self.connection_patch.start()

        self.tweeter_instance = Tweeter("test.db")
        self.tweeter_instance.user_id = 1  # Set a user ID to simulate a logged-in user

    def tearDown(self):
        self.connection_patch.stop()

    @patch("modules.Tweeter.Tweeter.start_screen")
    def test_logout(self, mock_start_screen):
        # Act: Call the logout method
        self.tweeter_instance.logout()

        # Assert: Check that the user ID was reset
        self.assertIsNone(self.tweeter_instance.user_id)

        # Assert: Check if the start_screen method was called
        mock_start_screen.assert_called_once()

if __name__ == '__main__':
    unittest.main()
