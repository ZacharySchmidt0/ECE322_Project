import unittest
import datetime
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter

class TestInsertRetweetMethod(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test.db'
        self.tweeter = Tweeter(self.test_db)
        self.tweeter.user_id = 1  # Simulating a logged-in user

    def tearDown(self):
        self.tweeter.conn.close()
        import os
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_insert_retweet(self):
        tweet_id = 123

        # Mock the database cursor's execute method
        self.tweeter.c.execute = MagicMock()

        # Call the method to be tested
        self.tweeter.insert_retweet(tweet_id)

        # Verifying that the correct SQL query was executed
        self.tweeter.c.execute.assert_called_once_with(
            """INSERT INTO retweets (usr, tid, rdate) VALUES (?, ?, ?);""",
            (self.tweeter.user_id, tweet_id, datetime.date.today())
        )

if __name__ == '__main__':
    unittest.main()
