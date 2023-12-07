import unittest
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter

class TestGetNextTweetId(unittest.TestCase):
    def setUp(self):
        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.connection_patch = patch('modules.Tweeter.sqlite3.connect', return_value=self.mock_connection)
        self.connection_patch.start()

        self.tweeter_instance = Tweeter("test.db")

    def tearDown(self):
        self.connection_patch.stop()

    def test_get_next_tweet_id(self):
        # Arrange: Mock the database response for the maximum tweet ID
        max_tid = 42
        self.mock_cursor.fetchone.return_value = (max_tid,)

        # Act: Call the get_next_tweet_id method
        next_tid = self.tweeter_instance.get_next_tweet_id()

        # Assert: Check that the execute method was called with the correct SQL query
        self.mock_cursor.execute.assert_called_once_with("SELECT MAX(tid) FROM tweets")

        # Assert: Check that the returned tweet ID is the next sequential ID
        self.assertEqual(next_tid, max_tid + 1)

if __name__ == '__main__':
    unittest.main()
