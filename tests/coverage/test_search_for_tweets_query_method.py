import unittest
from unittest.mock import MagicMock
from modules.Tweeter import Tweeter

class TestSearchForTweetsQueryMethod(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test.db'
        self.tweeter = Tweeter(self.test_db)

    def tearDown(self):
        self.tweeter.conn.close()
        import os
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_search_for_tweets_query(self):
        hashtag_keywords = ['hashtag1', 'hashtag2']
        text_keywords = ['keyword1', 'keyword2']
        page = 1
        page_size = 5
        offset = page * page_size

        # Mock the database cursor's methods
        self.tweeter.c.execute = MagicMock()
        self.tweeter.c.fetchall = MagicMock(return_value=[(1, 'Test tweet', '2023-01-01', 'User1')])

        # Call the method to be tested
        tweets = self.tweeter.search_for_tweets_query(hashtag_keywords, text_keywords, page, page_size)

        # Verifying that the correct SQL query was executed
        self.tweeter.c.execute.assert_called_once()
        args, kwargs = self.tweeter.c.execute.call_args
        self.assertIn("SELECT tid FROM mentions WHERE LOWER(term) = LOWER(?)", args[0])
        self.assertIn("SELECT tid FROM tweets WHERE LOWER(text) LIKE LOWER(?)", args[0])
        self.assertIn(f"LIMIT {page_size} OFFSET {offset}", args[0])
        self.assertEqual(len(args[1]), len(hashtag_keywords) + len(text_keywords) + 1)  # Parameters for query

        # Verifying that tweets are returned correctly
        self.assertEqual(tweets, [(1, 'Test tweet', '2023-01-01', 'User1')])

if __name__ == '__main__':
    unittest.main()
