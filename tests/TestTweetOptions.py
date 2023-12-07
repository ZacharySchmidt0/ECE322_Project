import unittest
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter

class TestTweetOptions(unittest.TestCase):
    def setUp(self):
        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.connection_patch = patch('modules.Tweeter.sqlite3.connect', return_value=self.mock_connection)
        self.connection_patch.start()

        # Mock the user ID to simulate a logged-in user
        self.user_id = 1
        self.tweeter_instance = Tweeter("test.db")
        self.tweeter_instance.user_id = self.user_id

    def tearDown(self):
        self.connection_patch.stop()

    @patch('modules.Tweeter.inquirer.select')
    def test_tweet_options(self, mock_select):
        # Arrange: Mock the inquirer select call to simulate user input
        # Simulate selecting different options
        mock_select.return_value.execute.side_effect = [
            'rep',  # reply to tweet
            'ret',  # retweet
            'x'     # exit the tweet options
        ]

        # Mock tweet statistics
        self.tweeter_instance.get_tweet_statistics = MagicMock(return_value=(5, 10))  # 5 retweets, 10 replies

        # Patch methods for reply and retweet
        with patch.object(self.tweeter_instance, 'compose_tweet') as mock_compose_tweet, \
             patch.object(self.tweeter_instance, 'insert_retweet') as mock_insert_retweet:

            # Act: Call the tweet_options method
            self.tweeter_instance.tweet_options(123)  # 123 is the example tweet ID

            # Assert: Check that the corresponding methods were called
            mock_compose_tweet.assert_called_once()
            mock_insert_retweet.assert_called_once_with(123)


if __name__ == '__main__':
    unittest.main()
