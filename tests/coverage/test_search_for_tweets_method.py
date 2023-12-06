
import unittest
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter, Choice

class TestSearchForTweetsMethod(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test.db'
        self.tweeter = Tweeter(self.test_db)

    def tearDown(self):
        self.tweeter.conn.close()
        import os
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    @patch('InquirerPy.inquirer.text.execute')
    @patch('InquirerPy.inquirer.select.execute')
    @patch('builtins.print')
    @patch('time.sleep')
    def test_search_for_tweets(self, mock_sleep, mock_print, mock_select, mock_text):
        mock_text.return_value = "Test #hashtag"
        mock_select.return_value = "x"

        with patch.object(Tweeter, 'search_for_tweets_query', return_value=[(1, 'Test tweet', '2023-01-01', 'User1')]) as mock_search_query, \
             patch.object(Tweeter, 'function_menu') as mock_function_menu:

            self.tweeter.search_for_tweets()

            mock_search_query.assert_called_once_with(['hashtag'], ['Test'], page=0, page_size=5)
            mock_function_menu.assert_called_once()

    @patch('InquirerPy.inquirer.text.execute')
    @patch('InquirerPy.inquirer.select.execute')
    @patch('builtins.print')
    @patch('time.sleep')
    # Test for navigating to the next page of tweets
    def test_next_page(self, mock_sleep, mock_print, mock_select_execute, mock_text_execute):
        mock_text_execute.return_value = "Test #hashtag"
        mock_select_execute.side_effect = ['n', 'x']  # Simulate selecting "Next Page" and then "Return to Function Menu"

        # Simulate the first page and second page having tweets
        with patch.object(Tweeter, 'search_for_tweets_query', side_effect=[[(1, 'Test tweet', '2023-01-01', 'User1')], [(2, 'Another tweet', '2023-01-02', 'User2')]]) as mock_search_query, \
             patch.object(Tweeter, 'function_menu') as mock_function_menu:

            tweeter = Tweeter('test.db')  # Or however your Tweeter object is initialized
            tweeter.search_for_tweets()

            # Verifying that search_for_tweets_query is called twice for two pages
            self.assertEqual(mock_search_query.call_count, 2)
            mock_function_menu.assert_called_once()


    @patch('InquirerPy.inquirer.text.execute')
    @patch('InquirerPy.inquirer.select.execute')
    @patch('builtins.print')
    @patch('time.sleep')
    # Test for selecting a tweet
    def test_select_tweet(self, mock_sleep, mock_print, mock_select_execute, mock_text_execute):
        mock_text_execute.return_value = "Test #hashtag"
        tweet_id = 1
        mock_select_execute.side_effect = [tweet_id, 'x']  # Simulate selecting a tweet and then "Return to Function Menu"

        with patch.object(Tweeter, 'search_for_tweets_query', return_value=[(tweet_id, 'Test tweet', '2023-01-01', 'User1')]) as mock_search_query, \
             patch.object(Tweeter, 'tweet_options') as mock_tweet_options, \
             patch.object(Tweeter, 'function_menu') as mock_function_menu:

            tweeter = Tweeter('test.db')  # Or however your Tweeter object is initialized
            tweeter.search_for_tweets()

            # Verifying that tweet_options is called for the selected tweet
            mock_tweet_options.assert_called_once_with(tweet_id)
            mock_function_menu.assert_called_once()

    @patch('InquirerPy.inquirer.text.execute')
    @patch('InquirerPy.inquirer.select.execute')
    @patch('builtins.print')
    @patch('time.sleep')
    # Test for navigating to the previous page of tweets
    def test_previous_page(self, mock_sleep, mock_print, mock_select_execute, mock_text_execute):
        mock_text_execute.return_value = "Test #hashtag"
        mock_select_execute.side_effect = ['n', 'p',
                                           'x']  # Simulate selecting "Next Page", "Previous Page", and then "Return to Function Menu"

        # Simulate each call to search_for_tweets_query returning at least one tweet
        with patch.object(Tweeter, 'search_for_tweets_query', side_effect=[
            [(1, 'Test tweet', '2023-01-01', 'User1')],  # First page
            [(2, 'Another tweet', '2023-01-02', 'User2')],  # Second page (next page)
            [(3, 'Yet another tweet', '2023-01-03', 'User3')]  # First page again (previous page)
        ]) as mock_search_query, \
                patch.object(Tweeter, 'function_menu') as mock_function_menu:
            self.tweeter.search_for_tweets()

            # Verifying that search_for_tweets_query is called three times for next page, previous page, and then previous page again
            self.assertEqual(mock_search_query.call_count, 3)
            mock_function_menu.assert_called_once()


if __name__ == '__main__':
    unittest.main()
