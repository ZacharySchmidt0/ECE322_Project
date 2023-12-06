import unittest
import sqlite3
from unittest.mock import patch
from modules.Tweeter import Tweeter

class TestLoginMethod(unittest.TestCase):
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
        # Adjusting table creation to match your schema
        self.tweeter.c.execute('''CREATE TABLE IF NOT EXISTS users (
                                    usr INT PRIMARY KEY,
                                    pwd TEXT,
                                    name TEXT,
                                    email TEXT,
                                    city TEXT,
                                    timezone FLOAT)''')
        # Inserting a test user with an integer ID
        self.tweeter.c.execute('''INSERT INTO users (usr, pwd) VALUES (?, ?)''', (123, 'testpass'))
        self.tweeter.conn.commit()

    @patch('InquirerPy.inquirer.text')
    @patch('InquirerPy.inquirer.secret')
    @patch('rich.rprint')
    @patch('time.sleep')
    def test_login_fail(self, mock_sleep, mock_rprint, mock_secret, mock_text):
        mock_text.return_value.execute.return_value = '999'  # Non-existing user ID
        mock_secret.return_value.execute.return_value = 'wrongpass'
        with patch.object(Tweeter, 'start_screen') as mock_start_screen:
            self.tweeter.login()
            mock_rprint.assert_called_with('[red]ERROR: Incorrect User Id or Password[red]\n')
            mock_start_screen.assert_called_once()

    @patch('InquirerPy.inquirer.text')
    @patch('InquirerPy.inquirer.secret')
    def test_login_success(self, mock_secret, mock_text):
        mock_text.return_value.execute.return_value = '123'  # Existing user ID
        mock_secret.return_value.execute.return_value = 'testpass'
        with patch.object(Tweeter, 'follow_feed') as mock_follow_feed:
            self.tweeter.login()
            self.assertEqual(self.tweeter.user_id, 123)  # Expecting integer user ID
            mock_follow_feed.assert_called_once()

if __name__ == '__main__':
    unittest.main()
