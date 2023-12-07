import unittest
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter

class TestTweeterFollowFeed(unittest.TestCase):
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

    @patch('modules.Tweeter.inquirer.select')
    def test_follow_feed(self, mock_select):
        expected_tweets = [
            (1, None, 'Tweet text 1', '2023-01-01', 'tweet', 'user1'),
            (2, None, 'Tweet text 2', '2023-01-02', 'retweet', 'user2')
        ]
        self.mock_cursor.fetchall.return_value = expected_tweets

        mock_select.return_value.execute.return_value = 'x' 

        self.tweeter_instance.follow_feed()

        self.mock_cursor.execute.assert_called_with(
            """\n            SELECT id, replyto, text, date, type, author FROM (
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
        """,
            (self.user_id, self.user_id, 5, 0)  
        )
        self.mock_cursor.fetchall.assert_called_once()

if __name__ == '__main__':
    unittest.main()
