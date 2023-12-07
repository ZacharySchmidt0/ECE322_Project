import unittest
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter

class TestTweeterFunctionMenu(unittest.TestCase):
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
    def test_function_menu_search_for_tweets(self, mock_select):
        # Arrange: Simulate selecting 'Search for tweets'
        mock_select.return_value.execute.side_effect = [
            'Follow Feed',
            'Search for tweets',
            'Search for users',
            'Compose a tweet',
            'List followers',
            'Logout'
        ]
        
        # Patch the methods that could be called by function_menu
        with patch.object(self.tweeter_instance, 'follow_feed') as mock_follow_feed:
            self.tweeter_instance.function_menu()
            mock_follow_feed.assert_called_once()
            
        with patch.object(self.tweeter_instance, 'search_for_tweets') as mock_search_for_tweets:
            self.tweeter_instance.function_menu()
            mock_search_for_tweets.assert_called_once()
            
        with patch.object(self.tweeter_instance, 'search_for_users') as mock_search_for_users:
            self.tweeter_instance.function_menu()
            mock_search_for_users.assert_called_once()
            
        with patch.object(self.tweeter_instance, 'compose_tweet') as mock_compose_tweet:
            self.tweeter_instance.function_menu()
            mock_compose_tweet.assert_called_once()
          
        with patch.object(self.tweeter_instance, 'list_followers') as mock_list_followers:
            self.tweeter_instance.function_menu()
            mock_list_followers.assert_called_once()
          
        with patch.object(self.tweeter_instance, 'logout') as mock_logout:
            self.tweeter_instance.function_menu()
            mock_logout.assert_called_once()


if __name__ == '__main__':
    unittest.main()
