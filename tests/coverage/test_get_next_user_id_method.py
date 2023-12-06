import unittest
import sqlite3
from modules.Tweeter import Tweeter

class TestGetNextUserIdMethod(unittest.TestCase):
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

    def test_next_user_id_empty_table(self):
        # Test when the users table is empty
        next_id = self.tweeter.get_next_user_id()
        self.assertEqual(next_id, 1)

    def test_next_user_id_with_existing_users(self):
        # Insert a user to simulate an existing user
        self.tweeter.c.execute('''INSERT INTO users (usr, pwd, name, email, city, timezone) VALUES (?, ?, ?, ?, ?, ?)''', 
                               (100, 'testpass', 'Test Name', 'test@example.com', 'Test City', 1.0))
        self.tweeter.conn.commit()

        # Test with existing users in the table
        next_id = self.tweeter.get_next_user_id()
        self.assertEqual(next_id, 101)

if __name__ == '__main__':
    unittest.main()
