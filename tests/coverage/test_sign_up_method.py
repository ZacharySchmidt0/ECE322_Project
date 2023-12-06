import unittest
import sqlite3
from unittest.mock import patch
from modules.Tweeter import Tweeter

class TestSignUpMethod(unittest.TestCase):
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
        # Creating users table to match your schema
        self.tweeter.c.execute('''CREATE TABLE IF NOT EXISTS users (
                                    usr INT PRIMARY KEY,
                                    pwd TEXT,
                                    name TEXT,
                                    email TEXT,
                                    city TEXT,
                                    timezone FLOAT)''')
        self.tweeter.conn.commit()

    @patch('InquirerPy.inquirer.text')
    @patch('InquirerPy.inquirer.secret')
    @patch('builtinsprint')
    @patch('time.sleep')
    def test_sign_up(self, mock_sleep, mock_print, mock_secret, mock_text):
        mock_text.side_effect = ['Test Name', 'test@email.com', 'Test City', '2.0']
        mock_secret.return_value.execute.return_value = 'testpass'
        with patch.object(Tweeter, 'insert_user') as mock_insert_user, \
             patch.object(Tweeter, 'get_next_user_id', return_value=123), \
             patch.object(Tweeter, 'start_screen') as mock_start_screen:

            self.tweeter.sign_up()

            # Check if insert_user was called with correct arguments
            mock_insert_user.assert_called_once_with('testpass', 'Test Name', 'test@email.com', 'Test City', 2.0)

            # Check if user ID was printed correctly
            mock_print.assert_any_call("Your User Id is: 122")

            # Check if it returns to start screen
            mock_start_screen.assert_called_once()

if __name__ == '__main__':
    unittest.main()
