import unittest
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter

class TestTweeterSignUp(unittest.TestCase):
    def setUp(self):
        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.connection_patch = patch('modules.Tweeter.sqlite3.connect', return_value=self.mock_connection)
        self.connection_patch.start()

    @patch('modules.Tweeter.inquirer.text')
    @patch('modules.Tweeter.inquirer.secret')
    @patch("modules.Tweeter.Tweeter.start_screen")
    def test_sign_up(self, mocked_start_screen, mock_secret, mock_text):
        # Arrange: Mock user input for sign up fields
        mock_text.return_value.execute.side_effect = ['John Doe', 'johndoe@example.com', 'Anytown', '1.0']
        mock_secret.return_value.execute.return_value = 'testpass'

        def exit_program():
                return 1
        mocked_start_screen.side_effect = exit_program
        with patch.object(Tweeter, 'insert_user') as mock_insert_user:
            tweeter_instance = Tweeter("test.db")
            tweeter_instance.sign_up()
            mock_insert_user.assert_called_once_with('testpass', 'John Doe', 'johndoe@example.com', 'Anytown', 1.0)

        
if __name__ == '__main__':
    unittest.main()
