import unittest
from unittest.mock import patch
from TweeterMutantA import Tweeter

class TestTweeter(unittest.TestCase):
    def setUp(self):
        self.tweeter = Tweeter("test.db")

    @patch('TweeterMutantA.inquirer.text')
    @patch('TweeterMutantA.inquirer.secret')
    @patch('TweeterMutantA.sqlite3.Cursor')
    def test_login_success(self, mock_cursor, mock_secret, mock_text):
        # Mocking successful login scenario
        mock_text.return_value.execute.return_value = "user123"
        mock_secret.return_value.execute.return_value = "password"
        mock_cursor.fetchone.return_value = ["user123"]
        self.tweeter.c = mock_cursor
        with patch.object(self.tweeter, 'follow_feed', return_value=None) as mock_follow_feed:
            self.tweeter.login()
            mock_follow_feed.assert_called_once()

    @patch('TweeterMutantA.inquirer.text')
    @patch('TweeterMutantA.sqlite3.Cursor')
    def test_sign_up(self, mock_cursor, mock_text):
        # Mocking inputs for sign up
        mock_text.side_effect = ["John Doe", "john@example.com", "New York", "3.5", "password123"]
        mock_cursor.fetchone.return_value = [None]
        mock_cursor.lastrowid = 1

        self.tweeter.c = mock_cursor
        with patch.object(self.tweeter, 'get_next_user_id', return_value=1):
            self.tweeter.sign_up()
            self.assertEqual(self.tweeter.user_id, 1)

    @patch('TweeterMutantA.sqlite3.Cursor')
    def test_follow_user(self, mock_cursor):
        # Mocking follow user functionality
        self.tweeter.user_id = 1
        follow_user_id = 2
        mock_cursor.fetchone.return_value = None

        self.tweeter.c = mock_cursor
        self.tweeter.follow_user(follow_user_id)
        mock_cursor.execute.assert_called_with("""INSERT INTO follows (flwer, flwee, start_date) VALUES (?, ?, ?);""",
                                               (self.tweeter.user_id, follow_user_id, ANY))

if __name__ == '__main__':
    unittest.main()
