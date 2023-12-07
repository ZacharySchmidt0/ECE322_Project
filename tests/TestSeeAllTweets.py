import unittest
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter

class TestSeeAllTweets(unittest.TestCase):
    def setUp(self):
        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.connection_patch = patch('modules.Tweeter.sqlite3.connect', return_value=self.mock_connection)
        self.connection_patch.start()

        self.tweeter_instance = Tweeter("test.db")

    def tearDown(self):
        self.connection_patch.stop()

    @patch('modules.Tweeter.inquirer.select')  # Mock the select call for user interaction
    def test_see_all_tweets_before_user_interaction(self, mock_select):
        # Arrange
        viewed_user_id = 2
        fake_tweets = [
            (10, "Tweet text 1", "2023-01-01"),
            (11, "Tweet text 2", "2023-01-02")
        ]
        self.mock_cursor.fetchall.return_value = fake_tweets
        
        # Setup the mock_select to simulate the user pressing 'x' to exit
        mock_select.return_value.execute.return_value = 'x'

        # Act
        self.tweeter_instance.see_all_tweets(viewed_user_id)

        # Assert
        self.mock_cursor.execute.assert_called_once_with(   
       """
        SELECT tid, text, tdate
        FROM tweets
        WHERE writer = ?
        ORDER BY tdate DESC;
        """, (viewed_user_id,)
        )
        self.mock_cursor.fetchall.assert_called_once()
        mock_select.assert_called()  # Check that user interaction was mocked

if __name__ == '__main__':
    unittest.main()
