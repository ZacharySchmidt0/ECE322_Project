import unittest
from unittest.mock import patch, MagicMock
import datetime
from modules.Tweeter import Tweeter

class TestComposeTweet(unittest.TestCase):
    def setUp(self):
        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.connection_patch = patch('modules.Tweeter.sqlite3.connect', return_value=self.mock_connection)
        self.connection_patch.start()

        self.tweeter_instance = Tweeter("test.db")
        self.tweeter_instance.user_id = 1  # Mocking a logged-in user with user_id 1

    def tearDown(self):
        self.connection_patch.stop()

    @patch('modules.Tweeter.inquirer.text')
    def test_compose_tweet(self, mock_text):
        # Arrange: Mock user input for the tweet's text
        tweet_text = "This is a test tweet"
        mock_text.return_value.execute.return_value = tweet_text
        current_date = datetime.date.today()

        # Act: Call the compose_tweet method
        self.tweeter_instance.compose_tweet()

        # Assert: Check that the insert_tweet method was called with the correct parameters
        with patch.object(self.tweeter_instance, 'insert_tweet') as mock_insert_tweet:
            self.tweeter_instance.compose_tweet()
            mock_insert_tweet.assert_called_once_with(
                self.tweeter_instance.user_id, current_date, tweet_text, replyto=None
            )

if __name__ == '__main__':
    unittest.main()
