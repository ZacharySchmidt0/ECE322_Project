import unittest
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter, Choice

class TestShowUserInfoMethod(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test.db'
        self.tweeter = Tweeter(self.test_db)

    def tearDown(self):
        self.tweeter.conn.close()
        import os
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    @patch('InquirerPy.inquirer.select')
    def test_show_user_info(self, mock_select):
        user_id = 1
        name = "Test User"

        # Mock database responses
        self.tweeter.c.execute = MagicMock()
        self.tweeter.c.fetchone = MagicMock(side_effect=[(10,), (5,), (3,)])
        self.tweeter.c.fetchall = MagicMock(return_value=[(123, 'Test Tweet', '2023-01-01')])

        # Mock user input for returning to user search
        mock_select.return_value.execute.return_value = 'x'

        self.tweeter.show_user_info(user_id, name)

        # Verify SQL queries were executed correctly
        self.tweeter.c.execute.assert_any_call("SELECT COUNT(*) FROM tweets WHERE writer = ?;", (user_id,))
        self.tweeter.c.execute.assert_any_call("SELECT COUNT(*) FROM follows WHERE flwer = ?;", (user_id,))
        self.tweeter.c.execute.assert_any_call("SELECT COUNT(*) FROM follows WHERE flwee = ?;", (user_id,))
        self.tweeter.c.execute.assert_any_call(
            """SELECT tid, text, tdate FROM tweets WHERE writer = ? ORDER BY tdate DESC LIMIT 3;""", 
            (user_id,))

        # Verify that the method exits correctly
        mock_select.assert_called_once()


    # Test for selecting a tweet
    @patch('InquirerPy.inquirer.select')
    def test_select_tweet(self, mock_select):
        user_id = 1
        name = "Test User"

        self.tweeter.c.execute = MagicMock()
        self.tweeter.c.fetchall = MagicMock(return_value=[(123, 'Test Tweet', '2023-01-01')])

        mock_select.side_effect = [Choice(123, "Tweet Info"), Choice('x', "Return to user search")]

        with patch.object(Tweeter, 'tweet_options') as mock_tweet_options:
            self.tweeter.show_user_info(user_id, name)
            mock_tweet_options.assert_called_once_with(123)

    # Test for following a user
    @patch('InquirerPy.inquirer.select')
    def test_follow_user(self, mock_select):
        user_id = 1
        name = "Test User"

        self.tweeter.c.execute = MagicMock()

        mock_select.side_effect = [Choice('f', "Follow this user"), Choice('x', "Return to user search")]

        with patch.object(Tweeter, 'follow_user') as mock_follow_user:
            self.tweeter.show_user_info(user_id, name)
            mock_follow_user.assert_called_once_with(user_id)

    # Test for seeing all tweets from a user
    @patch('InquirerPy.inquirer.select')
    def test_see_all_tweets(self, mock_select):
        user_id = 1
        name = "Test User"

        self.tweeter.c.execute = MagicMock()

        mock_select.side_effect = [Choice('s', "See all tweets from this user"), Choice('x', "Return to user search")]

        with patch.object(Tweeter, 'see_all_tweets') as mock_see_all_tweets:
            self.tweeter.show_user_info(user_id, name)
            mock_see_all_tweets.assert_called_once_with(user_id)

if __name__ == '__main__':
    unittest.main()
