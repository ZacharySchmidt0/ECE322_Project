import unittest
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter

class TestSearchForTweetsQuery(unittest.TestCase):
    def setUp(self):
        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.connection_patch = patch('modules.Tweeter.sqlite3.connect', return_value=self.mock_connection)
        self.connection_patch.start()

        self.tweeter_instance = Tweeter("test.db")

    def tearDown(self):
        self.connection_patch.stop()

    def test_search_for_tweets_query(self):
        # Arrange: Set up the input parameters for the method
        hashtag_keywords = ["#test"]
        text_keywords = ["example"]
        page = 0
        page_size = 5

        # Set up the expected fake results
        fake_tweets = [
            (1, "Sample tweet text 1", "2023-01-01", "user1"),
        ]
        self.mock_cursor.fetchall.return_value = fake_tweets

        # Act: Call the search_for_tweets_query method
        result = self.tweeter_instance.search_for_tweets_query(hashtag_keywords, text_keywords, page, page_size)

        # Assert: Check that the execute method was called with the correct SQL query
        self.mock_cursor.execute.assert_called()

        # Assert: Check that the returned result matches the fake data
        self.assertEqual(result, fake_tweets)

if __name__ == '__main__':
    unittest.main()
