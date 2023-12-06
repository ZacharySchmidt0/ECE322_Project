
import unittest
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter, Choice

class TestSeeAllTweetsMethod(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test.db'
        self.tweeter = Tweeter(self.test_db)

    def tearDown(self):
        self.tweeter.conn.close()
        import os
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    @patch('InquirerPy.inquirer.select')
    def test_see_all_tweets(self, mock_select):
        user_id = 1

        # Mock database responses
        self.tweeter.c.execute = MagicMock()
        self.tweeter.c.fetchall = MagicMock(return_value=[(123, 'Test Tweet', '2023-01-01')])

        # Mock user input for selecting a tweet and then exiting
        mock_select.side_effect = [Choice(123, "Tweet Info"), Choice('x', "Return to User Info")]

        with patch.object(Tweeter, 'tweet_options') as mock_tweet_options:
            self.tweeter.see_all_tweets(user_id)

            # Verify that tweet_options is called for the selected tweet
            mock_tweet_options.assert_called_once_with(123)

    @patch('InquirerPy.inquirer.select')
    @patch('builtins.print')
    def test_no_tweets_to_display(self, mock_print, mock_select):
        user_id = 1

        # Mock database responses with no tweets
        self.tweeter.c.execute = MagicMock()
        self.tweeter.c.fetchall = MagicMock(return_value=[])

        # Mock user input for exiting when no tweets are available
        mock_select.return_value.execute.return_value = 'x'

        self.tweeter.see_all_tweets(user_id)

        # Verify that a message is printed indicating no tweets are available
        mock_print.assert_called_with("No tweets available for this user.")
        # Verify that the user is given the option to exit
        mock_select.assert_called_once()

if __name__ == '__main__':
    unittest.main()
