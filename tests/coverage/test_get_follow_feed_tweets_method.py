import unittest
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter

class TestGetFollowFeedTweetsMethod(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test.db'
        self.tweeter = Tweeter(self.test_db)
        self.tweeter.user_id = 1  # Simulating a logged-in user

    def tearDown(self):
        self.tweeter.conn.close()
        import os
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_get_follow_feed_tweets(self):
        page = 0
        page_size = 5
        offset = page * page_size

        # Mock database responses
        self.tweeter.c.execute = MagicMock()
        self.tweeter.c.fetchall = MagicMock(return_value=[(1, None, 'Test tweet', '2023-01-01', 'Tweet', 'User1')])

        tweets = self.tweeter.get_follow_feed_tweets(page, page_size)

        # Verifying correct execution of SQL query
        self.tweeter.c.execute.assert_called_once_with(
            """
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
            """, (self.tweeter.user_id, self.tweeter.user_id, page_size, offset)
        )

        # Verifying the fetched data
        self.assertEqual(tweets, [(1, None, 'Test tweet', '2023-01-01', 'Tweet', 'User1')])

if __name__ == '__main__':
    unittest.main()
