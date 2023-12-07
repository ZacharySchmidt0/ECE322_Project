import unittest
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter

class TestListFollowers(unittest.TestCase):
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
    def test_list_followers(self, mock_select):
        # Arrange: Set up the fake followers data
        fake_followers = [
            (2, "follower1", "follower1@example.com", "City1", 1.0, "2023-01-01"),
            (3, "follower2", "follower2@example.com", "City2", 2.0, "2023-01-02")
        ]
        self.mock_cursor.fetchall.return_value = fake_followers

        # Mock user input to simulate exiting the followers list
        mock_select.return_value.execute.return_value = 'x'  # Assuming 'Exit' is an option to leave the list

        # Act: Call the list_followers method
        self.tweeter_instance.list_followers()

        # Assert: Check that the correct query was executed
        self.mock_cursor.execute.assert_called_once_with(
            """SELECT usr, name, email, city, timezone, start_date FROM users, follows WHERE flwee = ? AND flwer = usr;""",
            (self.tweeter_instance.user_id,)
        )

if __name__ == '__main__':
    unittest.main()
