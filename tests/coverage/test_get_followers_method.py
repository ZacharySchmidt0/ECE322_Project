import unittest
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter

class TestGetFollowersMethod(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test.db'
        self.tweeter = Tweeter(self.test_db)
        self.tweeter.user_id = 1  # Simulating a logged-in user

    def tearDown(self):
        self.tweeter.conn.close()
        import os
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_get_followers(self):
        # Mock database responses
        self.tweeter.c.execute = MagicMock()
        self.tweeter.c.fetchall = MagicMock(return_value=[(2, 'Jane Doe', 'jane@example.com', 'City', 1.0, '2023-01-01')])

        followers = self.tweeter.get_followers()

        # Verifying correct execution of SQL query
        self.tweeter.c.execute.assert_called_once_with(
            """SELECT usr, name, email, city, timezone, start_date FROM users, follows WHERE flwee = ? AND flwer = usr;""",
            (self.tweeter.user_id,)
        )

        # Verifying the fetched data
        self.assertEqual(followers, [(2, 'Jane Doe', 'jane@example.com', 'City', 1.0, '2023-01-01')])

if __name__ == '__main__':
    unittest.main()
