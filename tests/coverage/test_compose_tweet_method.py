import unittest
import datetime
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter

class TestComposeTweetMethod(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test.db'
        self.tweeter = Tweeter(self.test_db)
        self.tweeter.user_id = 1  # Simulating a logged-in user

    def tearDown(self):
        self.tweeter.conn.close()
        import os
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    @patch('InquirerPy.inquirer.text.execute')
    @patch('builtins.print')
    @patch('time.sleep')
    def test_compose_tweet(self, mock_sleep, mock_print, mock_text_execute):
        mock_text_execute.return_value = "Test tweet"
        with patch.object(Tweeter, 'insert_tweet') as mock_insert_tweet:
            self.tweeter.compose_tweet()

            mock_insert_tweet.assert_called_once_with(self.tweeter.user_id, datetime.date.today(), "Test tweet",
                                                      replyto=None)
            mock_print.assert_called_with("Tweet Posted")

    @patch('InquirerPy.inquirer.text.execute')
    @patch('builtins.print')
    @patch('time.sleep')
    def test_compose_tweet_with_return_function(self, mock_sleep, mock_print, mock_text_execute):
        mock_text_execute.return_value = "Test tweet"
        with patch.object(Tweeter, 'insert_tweet') as mock_insert_tweet:
            return_function = MagicMock()
            self.tweeter.compose_tweet(return_to=return_function)

            mock_insert_tweet.assert_called_once_with(self.tweeter.user_id, datetime.date.today(), "Test tweet",
                                                      replyto=None)
            mock_print.assert_called_with("Tweet Posted")
            return_function.assert_called_once()


if __name__ == '__main__':
    unittest.main()
