import unittest
import sqlite3
from modules.Tweeter import Tweeter

class TestTweeterInit(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test.db'

    def tearDown(self):
        import os
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_init(self):
        tweeter = Tweeter(self.test_db)

        self.assertIsNotNone(tweeter.conn)
        self.assertIsInstance(tweeter.conn, sqlite3.Connection)
        self.assertIsNotNone(tweeter.c)
        self.assertIsInstance(tweeter.c, sqlite3.Cursor)
        self.assertIsNone(tweeter.user_id)

        # Ensure proper closure of the connection
        tweeter.conn.close()

if __name__ == '__main__':
    unittest.main()
