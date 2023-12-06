import unittest
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter, Choice

class TestTweetOptionsMethod(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test.db'
        self.tweeter = Tweeter(self.test_db)

    def tearDown(self):
        self.tweeter.conn.close()
        import os
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    @patch('InquirerPy.inquirer.select')
    @patch('builtins.print')
    @patch('time.sleep')
    def test_reply_to_tweet(self, mock_sleep, mock_print, mock_select):
        tweet_id = 123
        self.tweeter.get_tweet_statistics = MagicMock(return_value=[10, 5])

        mock_select.side_effect = [Choice('rep', "Reply to this Tweet"), Choice('x', "Return")]

        with patch.object(Tweeter, 'compose_tweet') as mock_compose_tweet:
            self.tweeter.tweet_options(tweet_id)

            mock_compose_tweet.assert_called_once_with(replyto=tweet_id)
            mock_print.assert_called_with("Reply Successful")

    @patch('InquirerPy.inquirer.select')
    @patch('builtins.print')
    @patch('time.sleep')
    def test_retweet_tweet(self, mock_sleep, mock_print, mock_select):
        tweet_id = 123
        self.tweeter.get_tweet_statistics = MagicMock(return_value=[10, 5])

        mock_select.side_effect = [Choice('ret', "Retweet this Tweet"), Choice('x', "Return")]

        with patch.object(Tweeter, 'insert_retweet') as mock_insert_retweet:
            self.tweeter.tweet_options(tweet_id)

            mock_insert_retweet.assert_called_once_with(tweet_id)
            mock_print.assert_called_with("Retweet Successful")

    @patch('InquirerPy.inquirer.select')
    def test_return_from_tweet_options(self, mock_select):
        tweet_id = 123
        self.tweeter.get_tweet_statistics = MagicMock(return_value=[10, 5])

        # Simulating the user choosing to return ('x') from the tweet options
        mock_select.return_value.execute.return_value = 'x'

        self.tweeter.tweet_options(tweet_id)

        # Verifying that the inquirer.select was called with the correct choices
        mock_select.assert_called_once_with(
            message="Tweet Stats",
            choices=[
                Choice(None, "# of Retweets: 10"),
                Choice(None, "# of Replies: 5"),
                Choice('rep', "Reply to this Tweet"),
                Choice('ret', "Retweet this Tweet"),
                Choice('x', "Return")
            ]
        )

        # Ensure the method exits the loop when 'x' is selected
        self.assertEqual(mock_select.call_count, 1)

if __name__ == '__main__':
    unittest.main()
