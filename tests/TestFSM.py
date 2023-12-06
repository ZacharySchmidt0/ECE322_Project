import unittest
from unittest.mock import patch
from pathlib import Path
import sys
import sqlite3

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))
from modules.Tweeter import Tweeter

class TestTwitterEmulationFSM(unittest.TestCase):

    def setUp(self):
        self.twitter_emulation = Tweeter("example.db")

    @patch("modules.Tweeter.inquirer.select")
    @patch("modules.Tweeter.Tweeter.login")
    def test_transition_from_start_to_login_screen(self, mocked_login, mock_selection):
        mock_selection.return_value.execute.return_value = "Login"

        def exit_program():
            x = 1

        mocked_login.side_effect = exit_program

        self.twitter_emulation.start_screen()
        # Add assertions based on the expected state or behavior after the transition
        # Note: nothing to assert yet

    @patch("modules.Tweeter.inquirer.text")
    @patch("modules.Tweeter.inquirer.secret")
    @patch("modules.Tweeter.Tweeter.follow_feed")
    def test_transition_from_login_screen_to_registered_user(self, mocked_follow_feed, mocked_password, mock_text_input):
        mock_text_input.return_value.execute.return_value = "10"
        mocked_password.return_value.execute.return_value = "aaa"

        def exit_program():
            x = 1

        mocked_follow_feed.side_effect = exit_program

        self.twitter_emulation.login()
        self.assertEqual(self.twitter_emulation.user_id, "10")

    @patch("modules.Tweeter.inquirer.text")
    @patch("modules.Tweeter.inquirer.secret")
    @patch("modules.Tweeter.Tweeter.start_screen")
    def test_transition_from_login_screen_to_unregistered_user(self, mocked_start_screen, mocked_password, mock_text_input):
        username = "JohnDoe"
        try:
            mock_text_input.return_value.execute.side_effect = [username, "johndoe@gmail.com", "New York", "1"]
            mocked_password.return_value.execute.return_value = "newpwd12!"

            def exit_program():
                x = 1

            mocked_start_screen.side_effect = exit_program

            self.twitter_emulation.sign_up()

            self.assertEqual(self.twitter_emulation.conn.total_changes, 1)

            connection = sqlite3.connect("example.db")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE name = ?;", (username,))
            result = cursor.fetchone()
            self.assertIsNotNone(result)
            uid, pwd, uname, email, city, timezone = result
            self.assertEqual(pwd, "newpwd12!")
            self.assertEqual(uname, username)
            self.assertEqual(email, "johndoe@gmail.com")
            self.assertEqual(city, "New York")
            self.assertEqual(timezone, 1)
            connection.commit()
            connection.close()

        finally:
            connection = sqlite3.connect("example.db")
            cursor = connection.cursor()
            cursor.execute("DELETE FROM users WHERE name = ?;", (username,))
            connection.commit()
            connection.close()

    @patch("modules.Tweeter.inquirer.text")
    def test_transition_from_user_home_to_search_tweets(self, mock_text_input):
        mock_text_input.return_value = "search_tweets"
        self.twitter_emulation.user_home()
        # Add assertions based on the expected state or behavior after the transition

    """@patch("modules.Tweeter.inquirer.text")
    def test_transition_from_user_home_to_search_users(self, mock_text_input):
        mock_text_input.return_value = "search_users"
        self.twitter_emulation.user_home()
        # Add assertions based on the expected state or behavior after the transition

    @patch("modules.Tweeter.inquirer.text")
    def test_transition_from_user_home_to_compose_tweet(self, mock_text_input):
        mock_text_input.return_value = "compose_tweet"
        self.twitter_emulation.user_home()
        # Add assertions based on the expected state or behavior after the transition

    @patch("modules.Tweeter.inquirer.text")
    def test_transition_from_user_home_to_list_followers(self, mock_text_input):
        mock_text_input.return_value = "list_followers"
        self.twitter_emulation.user_home()
        # Add assertions based on the expected state or behavior after the transition

    @patch("modules.Tweeter.inquirer.text")
    def test_transition_from_user_home_to_logout(self, mock_text_input):
        mock_text_input.return_value = "logout"
        self.twitter_emulation.user_home()
        # Add assertions based on the expected state or behavior after the transition"""

if __name__ == "__main__":
    unittest.main()
