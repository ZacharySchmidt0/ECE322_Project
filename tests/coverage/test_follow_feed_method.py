import unittest
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter, Choice

class TestFollowFeedMethod(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test.db'
        self.tweeter = Tweeter(self.test_db)

    def tearDown(self):
        self.tweeter.conn.close()
        import os
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    @patch('InquirerPy.inquirer.select.execute')
    @patch('builtins.print')
    @patch('time.sleep')
    @patch.object(Tweeter, 'function_menu')
    def test_follow_feed(self, mock_function_menu, mock_sleep, mock_print, mock_select_execute):
        self.tweeter.get_follow_feed_tweets = MagicMock(
            return_value=[(1, None, 'Test tweet', '2023-01-01', 'Tweet', 'User1')])
        mock_select_execute.side_effect = ['x']  # Simulate selecting "Continue to Function Menu"

        self.tweeter.follow_feed()

        # Verifying the follow feed is displayed correctly
        mock_select_execute.assert_called_once()
        args, kwargs = mock_select_execute.call_args
        self.assertTrue(any(
            str(choice) == "User1 Replying to None: Test tweet (Date: 2023-01-01, Type: Tweet, Author: User1)" for
            choice in args[0]))

        # Verifying that function_menu is called
        mock_function_menu.assert_called_once()

    # Test for navigating to the next page of tweets
    @patch('InquirerPy.inquirer.select')
    @patch('builtins.print')
    @patch('time.sleep')
    def test_next_page(self, mock_sleep, mock_print, mock_select):
        self.tweeter.get_follow_feed_tweets = MagicMock(side_effect=[[], [(1, None, 'Test tweet', '2023-01-01', 'Tweet', 'User1')]])
        mock_select.side_effect = [Choice('n', "Next Page"), Choice('x', "Continue to Function Menu")]

        self.tweeter.follow_feed()

        # Verifying that get_follow_feed_tweets is called twice for two pages
        self.assertEqual(self.tweeter.get_follow_feed_tweets.call_count, 2)

    # Test for selecting a tweet
    @patch('InquirerPy.inquirer.select')
    @patch('time.sleep')
    def test_select_tweet(self, mock_sleep, mock_select):
        tweet_id = 1
        self.tweeter.get_follow_feed_tweets = MagicMock(return_value=[(tweet_id, None, 'Test tweet', '2023-01-01', 'Tweet', 'User1')])
        mock_select.side_effect = [Choice(tweet_id, "Tweet Info"), Choice('x', "Continue to Function Menu")]

        with patch.object(Tweeter, 'tweet_options') as mock_tweet_options:
            self.tweeter.follow_feed()

            # Verifying that tweet_options is called for the selected tweet
            mock_tweet_options.assert_called_once_with(tweet_id)

    # Test for navigating to the previous page of tweets
    @patch('InquirerPy.inquirer.select')
    @patch('time.sleep')
    def test_previous_page(self, mock_sleep, mock_select):
        self.tweeter.get_follow_feed_tweets = MagicMock(side_effect=[[], [(1, None, 'Test tweet', '2023-01-01', 'Tweet', 'User1')], []])
        mock_select.side_effect = [Choice('n', "Next Page"), Choice('p', "Previous Page"), Choice('x', "Continue to Function Menu")]

        self.tweeter.follow_feed()

        # Verifying that get_follow_feed_tweets is called three times for next, previous, and previous page again
        self.assertEqual(self.tweeter.get_follow_feed_tweets.call_count, 3)

if __name__ == '__main__':
    unittest.main()
