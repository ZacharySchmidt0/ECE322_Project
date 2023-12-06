import unittest
from datetime import date
from unittest.mock import patch, MagicMock
from Tweeter import Tweeter

class TestDataFlowTweeter(unittest.TestCase):
    def setUp(self):
        self.tweeter = Tweeter("test.db")
        self.tweeter.user_id = 1

    @patch('InquirerPy.inquirer.text')
    @patch('InquirerPy.inquirer.secret')
    def test_login_data_flow(self, mock_secret, mock_text):
        # Mock the user inputs for user ID and password
        mock_text.return_value.execute.return_value = "user123"
        mock_secret.return_value.execute.return_value = "password123"

        # Mock the database cursor to simulate a successful login
        self.tweeter.c = MagicMock()
        self.tweeter.c.execute.return_value = None
        self.tweeter.c.fetchone.return_value = ["user123"]

        # Execute the login function
        self.tweeter.login()

        # Check if user_id is set correctly after login
        self.assertEqual(self.tweeter.user_id, "user123")


    @patch('InquirerPy.inquirer.text')
    @patch('InquirerPy.inquirer.secret')
    def test_sign_up_data_flow(self, mock_secret, mock_text):
        # Mock the user inputs for sign-up details
        mock_text.side_effect = ["John Doe", "john@example.com", "New York", "3.5", "password123"]
        mock_secret.return_value.execute.return_value = "password123"

        # Mock the database cursor to simulate user sign-up
        self.tweeter.c = MagicMock()
        self.tweeter.get_next_user_id = MagicMock(return_value=1)
        self.tweeter.c.fetchone.return_value = [None]  # Simulate no existing user
        self.tweeter.c.lastrowid = 1

        # Execute the sign-up function
        self.tweeter.sign_up()

        # Check if user details are correctly passed to the database
        self.tweeter.c.execute.assert_called_with(
            '''INSERT INTO users (usr, pwd, name, email, city, timezone) VALUES (?, ?, ?, ?, ?, ?)''',
            (1, 'password123', 'John Doe', 'john@example.com', 'New York', 3.5)
        )

    @patch('InquirerPy.inquirer.text')
    @patch('InquirerPy.inquirer.secret')
    def test_follow_user_data_flow(self):
        follow_user_id = 2
        self.tweeter.c = MagicMock()
        self.tweeter.c.fetchone.return_value = None

        self.tweeter.follow_user(follow_user_id)
        self.tweeter.c.execute.assert_called_with(
            """INSERT INTO follows (flwer, flwee, start_date) VALUES (?, ?, ?);""",
            (self.tweeter.user_id, follow_user_id, datetime.date.today())
        )

if __name__ == '__main__':
    unittest.main()
