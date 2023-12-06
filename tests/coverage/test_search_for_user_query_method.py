import unittest
import sqlite3
from modules.Tweeter import Tweeter

class TestSearchForUserQueryMethod(unittest.TestCase):
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
        # Create users table and insert test data
        self.tweeter.c.execute('''CREATE TABLE IF NOT EXISTS users (
                                  usr INT PRIMARY KEY,
                                  pwd TEXT,
                                  name TEXT,
                                  email TEXT,
                                  city TEXT,
                                  timezone FLOAT)''')
        users_data = [
            (1, 'pass1', 'Alice', 'alice@example.com', 'Wonderland', 1.0),
            (2, 'pass2', 'Bob', 'bob@example.com', 'Babble', 2.0),
            (3, 'pass3', 'Charlie', 'charlie@example.com', 'Charm', 3.0)
        ]
        self.tweeter.c.executemany('''INSERT INTO users (usr, pwd, name, email, city, timezone) VALUES (?, ?, ?, ?, ?, ?)''', users_data)
        self.tweeter.conn.commit()

    def test_search_for_user_query_name_match(self):
        # Test for name match
        results = self.tweeter.search_for_user_query('Alice')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], 'Alice')

    def test_search_for_user_query_city_match(self):
        # Test for city match (and not name match)
        results = self.tweeter.search_for_user_query('Babble')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][3], 'Babble')

    def test_search_for_user_query_offset(self):
        # Test with an offset
        results = self.tweeter.search_for_user_query('a', offset=1)
        # Expecting at least one result, but not the first one
        self.assertGreaterEqual(len(results), 1)
        self.assertNotEqual(results[0][1], 'Alice')

if __name__ == '__main__':
    unittest.main()
