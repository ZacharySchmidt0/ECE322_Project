import unittest
from unittest.mock import patch, MagicMock
import datetime
from modules.Tweeter import Tweeter

class TestInsertTweet(unittest.TestCase):
    def setUp(self):
        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.connection_patch = patch('modules.Tweeter.sqlite3.connect', return_value=self.mock_connection)
        self.connection_patch.start()

        self.tweeter_instance = Tweeter("test.db")
        self.tweeter_instance.user_id = 1

    def tearDown(self):
        self.connection_patch.stop()

    def test_insert_tweet(self):
        # Arrange
        tweet_text = "Test tweet"
        current_date = datetime.date.today()
        replyto = None
        max_tid = 42
        self.mock_cursor.fetchone.return_value = (max_tid,)  # Mock return value for max(tid)

        # Act
        self.tweeter_instance.insert_tweet(self.tweeter_instance.user_id, current_date, tweet_text, replyto)

        # Assert
        # Check the call to get the maximum tid
        self.mock_cursor.execute.assert_any_call("SELECT MAX(tid) FROM tweets")

        # Check the call to insert the tweet
        new_tid = max_tid + 1  # Assuming the new tweet ID is max_tid + 1
        self.mock_cursor.execute.assert_any_call(
            """INSERT INTO tweets (tid, writer, tdate, text, replyto) Values (?, ?, ?, ?, ?);""",
            (new_tid, self.tweeter_instance.user_id, current_date, tweet_text, replyto)
        )

        # Check that commit was called on the connection
        self.mock_connection.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
