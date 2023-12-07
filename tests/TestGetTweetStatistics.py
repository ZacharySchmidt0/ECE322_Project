import unittest
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter

class TestGetTweetStatistics(unittest.TestCase):
    def setUp(self):
        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.connection_patch = patch('modules.Tweeter.sqlite3.connect', return_value=self.mock_connection)
        self.connection_patch.start()

        self.tweeter_instance = Tweeter("test.db")

    def tearDown(self):
        self.connection_patch.stop()

    def test_get_tweet_statistics(self):
        # Arrange: Mock the database response for retweets and replies count
        retweets_count = 5
        replies_count = 10
        self.mock_cursor.fetchone.side_effect = [(retweets_count,), (replies_count,)]

        tweet_id = 123  # Example tweet ID

        # Act: Call the get_tweet_statistics method
        retweets, replies = self.tweeter_instance.get_tweet_statistics(tweet_id)

        # Assert: Check that the correct query was executed for retweets
        self.mock_cursor.execute.assert_any_call(
            "SELECT COUNT(*) FROM retweets WHERE tid = ?", (tweet_id,)
        )

        # Assert: Check that the correct query was executed for replies
        self.mock_cursor.execute.assert_any_call(
            "SELECT COUNT(*) FROM tweets WHERE replyto = ?", (tweet_id,)
        )

        # Assert: Check that the returned counts are correct
        self.assertEqual(retweets, retweets_count)
        self.assertEqual(replies, replies_count)

if __name__ == '__main__':
    unittest.main()
