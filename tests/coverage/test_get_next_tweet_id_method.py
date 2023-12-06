import unittest
import sqlite3
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter

class TestGetNextTweetIdMethod(unittest.TestCase):
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
        self.tweeter.c.execute('''CREATE TABLE IF NOT EXISTS tweets (
                                  tid INT PRIMARY KEY,
                                  writer INT,
                                  tdate DATE,
                                  text TEXT,
                                  replyto INT)''')
        self.tweeter.conn.commit()

    def test_next_tweet_id_empty_table(self):
        # Test when the tweets table is empty
        self.tweeter.c.execute = MagicMock(return_value=None)
        self.tweeter.c.fetchone = MagicMock(return_value=[None])
        
        next_id = self.tweeter.get_next_tweet_id()
        self.assertEqual(next_id, 1)

    def test_next_tweet_id_with_existing_tweets(self):
        # Insert a tweet to simulate an existing tweet
        self.tweeter.c.execute('''INSERT INTO tweets (tid, writer, tdate, text) VALUES (?, ?, ?, ?)''', 
                               (100, 1, '2023-01-01', 'Test Tweet'))
        self.tweeter.conn.commit()

        # Mock fetchone to return a specific value
        self.tweeter.c.fetchone = MagicMock(return_value=[100])

        # Test with existing tweets in the table
        next_id = self.tweeter.get_next_tweet_id()
        self.assertEqual(next_id, 101)

if __name__ == '__main__':
    unittest.main()
