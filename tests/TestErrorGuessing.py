import unittest
from unittest.mock import patch, Mock

from pathlib import Path
import sys
import sqlite3

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))
from modules.Tweeter import Tweeter

class TestTwitterEmulator(unittest.TestCase):
    @patch("modules.Tweeter.inquirer.text")
    @patch("modules.Tweeter.inquirer.secret")
    @patch("modules.Tweeter.Tweeter.start_screen")
    def test_signup(self, mocked_start_screen, mocked_secret, mocked_text):
        # Mocking the behavior of InquirerPy's text prompt for the signup test case
        mocked_text.return_value.execute.side_effect = ["JohnDoe", "johndoe@gmail.com", "New York", "1"]

        # Mocking the behavior of InquirerPy's secret prompt for the password
        mocked_secret.return_value.execute.return_value = "password"

        # Mocking the behavior of start_screen to exit the program
        def exit_program():
            x = 1

        mocked_start_screen.side_effect = exit_program

        # Mocking the insert_user method to check if it's called
        with patch.object(Tweeter, 'insert_user') as mock_insert_user:
            twitter_emulator = Tweeter("example.db")
            twitter_emulator.sign_up()

            # Assert that the insert_user method is called with the expected arguments
            mock_insert_user.assert_called_once_with("password", "JohnDoe", "johndoe@gmail.com", "New York", 1)

    @patch("modules.Tweeter.inquirer.text")
    @patch("modules.Tweeter.inquirer.secret")
    @patch("modules.Tweeter.Tweeter.start_screen")
    def test_invalid_login(self, mocked_start_screen, mocked_text, mocked_secret):
        # Mocking the behavior of InquirerPy's text prompt for the login test case
        mocked_text.return_value.execute.side_effect = "JohnDoe"
        mocked_secret.return_value.execute.side_effect = "wrong_password"

        # Mocking the behavior of start_screen to exit the program
        def exit_program():
            x = 1

        mocked_start_screen.side_effect = exit_program

        twitter_emulator = Tweeter("example.db")
        twitter_emulator.login()

        # Assert that the user is not logged in after an invalid login attempt
        self.assertIsNone(twitter_emulator.user_id)

    @patch("modules.Tweeter.inquirer.text")
    @patch("modules.Tweeter.inquirer.secret")
    @patch("modules.Tweeter.Tweeter.follow_feed")
    def test_valid_login(self, mocked_follow_feed, mocked_secret, mocked_text):
        user_id = 1000
        password = "valid_password"
        try:
            # Helper method to insert a test user into the database
            connection = sqlite3.connect("example.db")
            cursor = connection.cursor()

            # Using parameterized query to prevent SQL injection
            cursor.execute("INSERT INTO users (usr, pwd) VALUES (?, ?)", (user_id, password))

            connection.commit()
            connection.close()

            # Mocking the behavior of InquirerPy's text and secret prompts for the login test case
            mocked_text.return_value.execute.return_value = str(user_id)
            mocked_secret.return_value.execute.return_value = password

            # Mocking the behavior of start_screen to exit the program
            def exit_program():
                x = 1

            mocked_follow_feed.side_effect = exit_program

            twitter_emulator = Tweeter("example.db")
            twitter_emulator.login()

            # Assert that the user is logged in after a valid login attempt
            self.assertIsNotNone(twitter_emulator.user_id)
            self.assertEqual(twitter_emulator.user_id, str(user_id))

        finally:
            connection = sqlite3.connect("example.db")
            cursor = connection.cursor()
            cursor.execute("DELETE FROM users WHERE usr = ?;", (user_id,))
            connection.commit()
            connection.close()

    """@patch("modules.Tweeter.inquirer.text")
    def test_compose_tweet(self, mocked_prompt):
        # Mocking the behavior of InquirerPy's prompt for the compose tweet test case
        mocked_prompt.return_value.execute.return_value = "Compose a tweet"

        twitter_emulator = Tweeter("example.db")
        twitter_emulator.user_id = "LoggedInUser"
        twitter_emulator.function_menu()

        # Assert that the selected option is "Compose a tweet"
        self.assertEqual(twitter_emulator.selected_option, "Compose a tweet")

    @patch("modules.Tweeter.inquirer.text")
    def test_search_tweets(self, mocked_prompt):
        # Mocking the behavior of InquirerPy's prompt for the search tweets test case
        mocked_prompt.return_value.execute.return_value = "Search for tweets"

        twitter_emulator = Tweeter("example.db")
        twitter_emulator.user_id = "LoggedInUser"
        twitter_emulator.function_menu()

        # Assert that the selected option is "Search for tweets"
        self.assertEqual(twitter_emulator.selected_option, "Search for tweets")

        # Mocking the behavior of InquirerPy's prompt for the search tweets screen
        mocked_prompt.return_value.execute.return_value = "Search Keywords"

        twitter_emulator.search_for_tweets()

        # Assert that the keywords are set to "Search Keywords"
        self.assertEqual(twitter_emulator.keywords, "Search Keywords")

    @patch("modules.Tweeter.inquirer.text")
    def test_search_users(self, mocked_prompt):
        # Mocking the behavior of InquirerPy's prompt for the search users test case
        mocked_prompt.return_value.execute.return_value = "Search for users"

        twitter_emulator = Tweeter("example.db")
        twitter_emulator.user_id = "LoggedInUser"
        twitter_emulator.function_menu()

        # Assert that the selected option is "Search for users"
        self.assertEqual(twitter_emulator.selected_option, "Search for users")

        # Mocking the behavior of InquirerPy's prompt for the search users screen
        mocked_prompt.return_value.execute.return_value = "Search Keywords"

        twitter_emulator.search_for_users()

        # Assert that the keywords are set to "Search Keywords"
        self.assertEqual(twitter_emulator.keywords, "Search Keywords")

    @patch("modules.Tweeter.inquirer.text")
    def test_compose_tweet_input(self, mocked_text):
        # Mocking the behavior of InquirerPy's text prompt for the compose tweet input test case
        mocked_text.return_value.execute.return_value = "Test tweet"

        twitter_emulator = Tweeter("example.db")
        twitter_emulator.user_id = "LoggedInUser"
        twitter_emulator.compose_tweet()

        # Assert that the tweet text is set to "Test tweet"
        self.assertEqual(twitter_emulator.tweet_text, "Test tweet")

    @patch("modules.Tweeter.inquirer.text")
    def test_compose_tweet_length_limit(self, mocked_text):
        # Mocking the behavior of InquirerPy's text prompt for the compose tweet length limit test case
        mocked_text.return_value.execute.return_value = "Too Long Tweet" + "a" * 140

        twitter_emulator = Tweeter("example.db")
        twitter_emulator.user_id = "LoggedInUser"
        twitter_emulator.compose_tweet()

        # Assert that the tweet text is truncated to 140 characters
        self.assertEqual(len(twitter_emulator.tweet_text), 140)"""

if __name__ == "__main__":
    unittest.main()
