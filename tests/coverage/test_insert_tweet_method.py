import unittest
import datetime
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter

class TestInsertTweetMethod(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test.db'
        self.tweeter = Tweeter(self.test_db)

    def tearDown(self):
        self.tweeter.conn.close()
        import os
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    @patch('Tweeter.Tweeter.get_next_tweet_id', return_value=123)
    def test_insert_tweet(self, mock_get_next_tweet_id):
        writer = 1
        tdate = datetime.date.today()
        text = "This is a test tweet #test"
        replyto = None

        # Mock the database cursor's methods
        self.tweeter.c.execute = MagicMock()
        self.tweeter.c.fetchone = MagicMock(return_value=None)

        # Call the method to be tested
        self.tweeter.insert_tweet(writer, tdate, text, replyto)

        # Verifying that the correct SQL queries were executed
        self.tweeter.c.execute.assert_any_call(
            """INSERT INTO tweets (tid, writer, tdate, text, replyto) Values (?, ?, ?, ?, ?);""",
            (123, writer, tdate, text, replyto,)
        )
        self.tweeter.c.execute.assert_any_call("""SELECT * FROM hashtags WHERE term = ?""", ('test',))
        self.tweeter.c.execute.assert_any_call("""INSERT INTO hashtags VALUES (?)""", ('test',))
        self.tweeter.c.execute.assert_any_call("""SELECT * FROM mentions WHERE term = ? AND tid = ?""", ('test', 123))
        self.tweeter.c.execute.assert_any_call("""INSERT into mentions VALUES (?, ?)""", (123, 'test',))

if __name__ == '__main__':
    unittest.main()
