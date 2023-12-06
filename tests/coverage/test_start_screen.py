
import unittest
from unittest.mock import patch
from modules.Tweeter import Tweeter

class TestStartScreen(unittest.TestCase):
    def setUp(self):
        self.tweeter = Tweeter('test.db')

    def tearDown(self):
        self.tweeter.conn.close()

    @patch('InquirerPy.inquirer.select')
    def test_start_screen_login(self, mock_select):
        mock_select.return_value.execute.return_value = "Login"
        with patch.object(Tweeter, 'login') as mock_login:
            self.tweeter.start_screen()
            mock_login.assert_called_once()

    @patch('InquirerPy.inquirer.select')
    def test_start_screen_sign_up(self, mock_select):
        mock_select.return_value.execute.return_value = "Sign Up"
        with patch.object(Tweeter, 'sign_up') as mock_sign_up:
            self.tweeter.start_screen()
            mock_sign_up.assert_called_once()

    @patch('InquirerPy.inquirer.select')
    def test_start_screen_exit(self, mock_select):
        mock_select.return_value.execute.return_value = "Exit"
        with patch.object(Tweeter, 'quit') as mock_quit:
            self.tweeter.start_screen()
            mock_quit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
