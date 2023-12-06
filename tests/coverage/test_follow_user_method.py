import unittest
import datetime
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter

class TestFollowUserMethod(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test.db'
        self.tweeter = Tweeter(self.test_db)
        self.tweeter.user_id = 1  # Simulating a logged-in user

    def tearDown(self):
        self.tweeter.conn.close()
        import os
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    @patch('builtins.print')
    @patch('time.sleep')
    def test_follow_new_user(self, mock_sleep, mock_print):
        follow_user_id = 2
        self.tweeter.c.execute = MagicMock()
        self.tweeter.c.fetchone = MagicMock(return_value=None)

        self.tweeter.follow_user(follow_user_id)

        # Verifying that an INSERT operation was attempted
        self.tweeter.c.execute.assert_called_with(
            """INSERT INTO follows (flwer, flwee, start_date) VALUES (?, ?, ?);""",
            (1, follow_user_id, datetime.date.today())
        )
        mock_print.assert_called_with(f"You are now following user {follow_user_id}")

    @patch('builtins.print')
    @patch('time.sleep')
    def test_already_following_user(self, mock_sleep, mock_print):
        follow_user_id = 2
        self.tweeter.c.execute = MagicMock()
        self.tweeter.c.fetchone = MagicMock(return_value=(1, 2, datetime.date.today()))

        self.tweeter.follow_user(follow_user_id)

        # Verifying no INSERT operation was attempted after finding an existing follow relationship
        self.tweeter.c.execute.assert_called_once_with(
            """SELECT * FROM follows WHERE flwer = ? AND flwee = ?;""",
            (1, follow_user_id)
        )
        mock_print.assert_called_with(f"{self.tweeter.user_id} is already following {follow_user_id}")

if __name__ == '__main__':
    unittest.main()
