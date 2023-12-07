import unittest
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter


class TestTweeterStartScreen(unittest.TestCase):
    def setUp(self):
        self.tweeter_instance = Tweeter("test.db")

    @patch('modules.Tweeter.inquirer.select')
    def test_start_screen_login(self, mock_select):
        mock_select.return_value.execute.return_value = "Login"
        with patch.object(self.tweeter_instance, 'login') as mock_login:
            self.tweeter_instance.start_screen()
            mock_login.assert_called_once()

    @patch('modules.Tweeter.inquirer.select')
    def test_start_screen_sign_up(self, mock_select):
        mock_select.return_value.execute.return_value = "Sign Up"
        with patch.object(self.tweeter_instance, 'sign_up') as mock_sign_up:
            self.tweeter_instance.start_screen()
            mock_sign_up.assert_called_once()

    @patch('modules.Tweeter.inquirer.select')
    def test_start_screen_exit(self, mock_select):
        mock_select.return_value.execute.return_value = "Exit"
        with patch.object(self.tweeter_instance, 'quit') as mock_quit:
            self.tweeter_instance.start_screen()
            mock_quit.assert_called_once()
        