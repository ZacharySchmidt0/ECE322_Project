import unittest
import sqlite3
from unittest.mock import patch
from modules.Tweeter import Tweeter

class TestInsertUserMethod(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test.db'
        self.tweeter = Tweeter(self.test_db)
        self.create_test_data()

    def tearDown(self):
        self.tweeter.conn.close()
        import os
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def create_test_data(self):
        self.tweeter.c.execute('''CREATE TABLE IF NOT EXISTS users (
                                  usr INT PRIMARY KEY,
                                  pwd TEXT,
                                  name TEXT,
                                  email TEXT,
                                  city TEXT,
                                  timezone FLOAT)''')
        self.tweeter.conn.commit()

    @patch('Tweeter.Tweeter.get_next_user_id', return_value=123)
    def test_insert_user(self, mock_get_next_user_id):
        # Inserting a new user
        self.tweeter.insert_user('testpass', 'Test Name', 'test@example.com', 'Test City', 1.0)

        # Verifying the insertion
        self.tweeter.c.execute('SELECT * FROM users WHERE usr = 123')
        user = self.tweeter.c.fetchone()

        self.assertIsNotNone(user)
        self.assertEqual(user[0], 123)
        self.assertEqual(user[1], 'testpass')
        self.assertEqual(user[2], 'Test Name')
        self.assertEqual(user[3], 'test@example.com')
        self.assertEqual(user[4], 'Test City')
        self.assertEqual(user[5], 1.0)

if __name__ == '__main__':
    unittest.main()
