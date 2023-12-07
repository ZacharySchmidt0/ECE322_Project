import unittest
from unittest.mock import patch, MagicMock
import datetime
from modules.Tweeter import Tweeter

class TestInsertRetweet(unittest.TestCase):
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

    def test_insert_retweet(self):
        tweet_id = 123  # Example tweet ID
        current_date = datetime.date.today()

        # Act: Call the insert_retweet method
        self.tweeter_instance.insert_retweet(tweet_id)

        # Assert: Check that the execute method was called with the correct SQL and parameters
        self.mock_cursor.execute.assert_called_once_with(
            """INSERT INTO retweets (usr, tid, rdate) VALUES (?, ?, ?);""",
            (self.tweeter_instance.user_id, tweet_id, current_date)
        )

        # Assert: Check that commit was called on the connection
        self.mock_connection.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
