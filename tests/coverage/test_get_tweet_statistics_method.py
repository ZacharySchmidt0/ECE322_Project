import unittest
from unittest.mock import MagicMock
from modules.Tweeter import Tweeter

class TestGetTweetStatisticsMethod(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test.db'
        self.tweeter = Tweeter(self.test_db)

    def tearDown(self):
        self.tweeter.conn.close()
        import os
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_get_tweet_statistics(self):
        tweet_id = 123

        # Mock database responses
        self.tweeter.c.execute = MagicMock()
        self.tweeter.c.fetchone = MagicMock(side_effect=[(5,), (3,)])

        retweets_count, replies_count = self.tweeter.get_tweet_statistics(tweet_id)

        # Verifying correct execution of SQL queries
        self.tweeter.c.execute.assert_any_call("SELECT COUNT(*) FROM retweets WHERE tid = ?", (tweet_id,))
        self.tweeter.c.execute.assert_any_call("SELECT COUNT(*) FROM tweets WHERE replyto = ?", (tweet_id,))

        # Verifying the counts are returned correctly
        self.assertEqual(retweets_count, 5)
        self.assertEqual(replies_count, 3)

if __name__ == '__main__':
    unittest.main()
