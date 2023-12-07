import unittest
from unittest.mock import patch, MagicMock
import datetime
from modules.Tweeter import Tweeter

class TestFollowUser(unittest.TestCase):
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

    def test_follow_user(self):
        # Arrange: Set the user to be followed
        follow_user_id = 2

        # Mock the database response to indicate the user is not already being followed
        self.mock_cursor.fetchone.return_value = None

        # Act: Call the follow_user method
        self.tweeter_instance.follow_user(follow_user_id)

        # Assert: Check that the method checked if the user is already being followed
        self.mock_cursor.execute.assert_any_call(
            "SELECT * FROM follows WHERE flwer = ? AND flwee = ?;", 
            (self.tweeter_instance.user_id, follow_user_id)
        )

        # Assert: Check that the execute method was called with the correct SQL to insert the follow relationship
        current_date = datetime.date.today()
        self.mock_cursor.execute.assert_any_call(
            "INSERT INTO follows (flwer, flwee, start_date) VALUES (?, ?, ?);",
            (self.tweeter_instance.user_id, follow_user_id, current_date)
        )

        # Assert: Check that the commit was called on the connection
        self.mock_connection.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
