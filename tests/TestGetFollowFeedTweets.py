import unittest
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter

class TestTweeterGetFollowFeedTweets(unittest.TestCase):
    def setUp(self):
        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.connection_patch = patch('modules.Tweeter.sqlite3.connect', return_value=self.mock_connection)
        self.connection_patch.start()
        
        # Mock the user ID to simulate a logged-in user
        self.user_id = 1
        self.tweeter_instance = Tweeter("test.db")
        self.tweeter_instance.user_id = self.user_id  # Set the user ID as if logged in

    def tearDown(self):
        self.connection_patch.stop()

    def test_get_follow_feed_tweets(self):
        # Arrange: Prepare the expected SQL query and the fake result set
        expected_query = """
            SELECT id, replyto, text, date, type, author FROM (
                SELECT tweets.tid AS id, tweets.text, tweets.tdate AS date, 'tweet' AS type, tweets.writer AS author, replyto
                FROM tweets
                INNER JOIN follows ON tweets.writer = follows.flwee
                WHERE follows.flwer = ?
                UNION ALL
                SELECT tweets.tid AS id, tweets.text, retweets.rdate AS date, 'retweet' AS type, retweets.usr AS author, NULL as replyto
                FROM retweets
                INNER JOIN tweets ON retweets.tid = tweets.tid
                INNER JOIN follows ON retweets.usr = follows.flwee
                WHERE follows.flwer = ?
            ) ORDER BY date DESC LIMIT ? OFFSET ?;
        """
        fake_tweets = [
            (1, None, 'Sample tweet text', '2023-01-01', 'tweet', 'user1'),
            (2, None, 'Another sample tweet text', '2023-01-02', 'retweet', 'user2')
        ]
        self.mock_cursor.fetchall.return_value = fake_tweets

        # Act: Call the get_follow_feed_tweets method with a page number and page size
        page = 0
        page_size = 5
        result = self.tweeter_instance.get_follow_feed_tweets(page=page, page_size=page_size)

        # Assert: Check that the query was executed correctly
        self.mock_cursor.execute.assert_called_once_with(expected_query, (self.user_id, self.user_id, page_size, page * page_size))

        # Assert: Check that the result matches the fake tweets
        self.assertEqual(result, fake_tweets)

if __name__ == '__main__':
    unittest.main()
