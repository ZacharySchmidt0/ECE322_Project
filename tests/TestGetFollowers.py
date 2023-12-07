import unittest
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter

class TestGetFollowers(unittest.TestCase):
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

    def test_get_followers(self):
        # Arrange: Set up the expected fake followers data
        fake_followers = [
            (2, "Follower1", "follower1@example.com", "City1", 1.0, "2023-01-01"),
            (3, "Follower2", "follower2@example.com", "City2", 2.0, "2023-01-02")
        ]
        self.mock_cursor.fetchall.return_value = fake_followers

        # Act: Call the get_followers method
        followers = self.tweeter_instance.get_followers()

        # Assert: Check that the execute method was called with the correct SQL query
        self.mock_cursor.execute.assert_called_once_with(
            """SELECT usr, name, email, city, timezone, start_date FROM users, follows WHERE flwee = ? AND flwer = usr;""",
            (self.tweeter_instance.user_id,)
        )

        # Assert: Check that the returned followers list matches the fake data
        self.assertEqual(followers, fake_followers)

if __name__ == '__main__':
    unittest.main()
