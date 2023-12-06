import unittest
from unittest.mock import patch
from modules.Tweeter import Tweeter

class TestFunctionMenuMethod(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test.db'
        self.tweeter = Tweeter(self.test_db)

    def tearDown(self):
        self.tweeter.conn.close()
        import os
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    @patch('InquirerPy.inquirer.select')
    def test_follow_feed_choice(self, mock_select):
        mock_select.return_value.execute.return_value = "Follow Feed"
        with patch.object(Tweeter, 'follow_feed') as mock_follow_feed:
            self.tweeter.function_menu()
            mock_follow_feed.assert_called_once()

    # Similar tests for other choices
    # Example for "Search for tweets"
    @patch('InquirerPy.inquirer.select')
    def test_search_for_tweets_choice(self, mock_select):
        mock_select.return_value.execute.return_value = "Search for tweets"
        with patch.object(Tweeter, 'search_for_tweets') as mock_search_for_tweets:
            self.tweeter.function_menu()
            mock_search_for_tweets.assert_called_once()

    # Tests for "Search for users"
    @patch('InquirerPy.inquirer.select')
    def test_search_for_users_choice(self, mock_select):
        mock_select.return_value.execute.return_value = "Search for users"
        with patch.object(Tweeter, 'search_for_users') as mock_search_for_users:
            self.tweeter.function_menu()
            mock_search_for_users.assert_called_once()

    # Tests for "Compose a tweet"
    @patch('InquirerPy.inquirer.select')
    def test_compose_tweet_choice(self, mock_select):
        mock_select.return_value.execute.return_value = "Compose a tweet"
        with patch.object(Tweeter, 'compose_tweet') as mock_compose_tweet:
            self.tweeter.function_menu()
            mock_compose_tweet.assert_called_once()

    # Tests for "List followers"
    @patch('InquirerPy.inquirer.select')
    def test_list_followers_choice(self, mock_select):
        mock_select.return_value.execute.return_value = "List followers"
        with patch.object(Tweeter, 'list_followers') as mock_list_followers:
            self.tweeter.function_menu()
            mock_list_followers.assert_called_once()

    # Tests for "Logout"
    @patch('InquirerPy.inquirer.select')
    def test_logout_choice(self, mock_select):
        mock_select.return_value.execute.return_value = "Logout"
        with patch.object(Tweeter, 'logout') as mock_logout:
            self.tweeter.function_menu()
            mock_logout.assert_called_once()

if __name__ == '__main__':
    unittest.main()
