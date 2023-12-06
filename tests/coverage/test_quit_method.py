import unittest
import sqlite3
from unittest.mock import patch
from modules.Tweeter import Tweeter

class TestQuitMethod(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test.db'
        self.tweeter = Tweeter(self.test_db)

    def tearDown(self):
        # Just in case the connection is still open
        if self.tweeter.conn:
            self.tweeter.conn.close()
        import os
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    @patch('time.sleep')
    @patch('rich.rprint')
    @patch('builtins.exit')
    def test_quit(self, mock_exit, mock_rprint, mock_sleep):
        self.tweeter.quit()

        # Verifying the exit and print calls
        mock_exit.assert_called_once()
        mock_rprint.assert_called_with('[red]Exiting now[red]')

        # Verifying that the connection is closed
        self.assertTrue(self.tweeter.conn is None or self.tweeter.conn.closed)

if __name__ == '__main__':
    unittest.main()
