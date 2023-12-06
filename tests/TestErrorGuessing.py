import unittest
from unittest.mock import patch, Mock

from pathlib import Path
import sys
import sqlite3

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))
from modules.Tweeter import Tweeter

"""
Author: Zachary Schmidt

This class tests the main functions of the Tweeter app from the perspective of error guessing. Test cases were initially
developed by ChatGPT and then refined by the author.
"""
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

    @patch("modules.Tweeter.inquirer.text")
    @patch("modules.Tweeter.Tweeter.function_menu")
    def test_compose_tweet(self, mocked_function_menu, mocked_text):
        # Mocking the behavior of InquirerPy's prompt for the compose tweet test case
        tweet_text = "Compose a tweet"
        mocked_text.return_value.execute.return_value = tweet_text

        conn = sqlite3.connect("example.db")
        cursor = conn.cursor()

        # Mocking the behavior of start_screen to exit the program
        def exit_program():
            x = 1

        mocked_function_menu.side_effect = exit_program

        twitter_emulator = Tweeter("example.db")
        twitter_emulator.compose_tweet()
        twitter_emulator.user_id = "LoggedInUser"

        # Call the compose_tweet method to test
        twitter_emulator.compose_tweet()

        # Check if the tweet is inserted into the database correctly
        cursor.execute("SELECT * FROM tweets WHERE writer = 'LoggedInUser';")
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        tweet_id, writer, tdate, text, replyto = result
        self.assertEqual(writer, "LoggedInUser")
        # You may need to adjust these assertions based on the actual implementation
        self.assertIsNotNone(tdate)
        self.assertEqual(text, "Compose a tweet")
        self.assertIsNone(replyto)

        cursor.execute("DELETE FROM tweets WHERE text = ?;", (tweet_text,))
        conn.commit()
        conn.close()

    @patch("modules.Tweeter.inquirer.text")
    @patch("modules.Tweeter.inquirer.select")
    @patch("modules.Tweeter.Tweeter.function_menu")
    def test_search_tweets(self, mocked_function_menu, mocked_selection, mocked_prompt):
        twitter_emulator = Tweeter("example.db")
        twitter_emulator.user_id = "LoggedInUser"

        # Mocking the behavior of InquirerPy's prompt for the search tweets screen
        mocked_prompt.return_value.execute.return_value = "tweet1"
        mocked_selection.return_value.execute.return_value = "x"

        # Mocking the behavior of start_screen to exit the program
        def exit_program():
            x = 1

        mocked_function_menu.side_effect = exit_program

        twitter_emulator.search_for_tweets()

        for selection in mocked_selection.call_args_list[0][1]['choices']:
            selectionStr = selection.name
            if "Writer" in selectionStr:
                self.assertIn("tweet1", selectionStr)

    @patch("modules.Tweeter.inquirer.text")
    @patch("modules.Tweeter.inquirer.select")
    @patch("modules.Tweeter.Tweeter.function_menu")
    def test_search_users(self, mocked_function_menu, mocked_selection, mocked_prompt):
        twitter_emulator = Tweeter("example.db")
        twitter_emulator.user_id = "LoggedInUser"

        # Mocking the behavior of InquirerPy's prompt for the search users screen
        mocked_prompt.return_value.execute.return_value = "usr1"
        mocked_selection.return_value.execute.return_value = "x"

        # Mocking the behavior of start_screen to exit the program
        def exit_program():
            x = 1

        mocked_function_menu.side_effect = exit_program

        twitter_emulator.search_for_users()

        # Adjust the assertion based on the actual structure of the choices
        for selection in mocked_selection.call_args_list[0][1]['choices']:
            selectionStr = selection.name
            if "User ID" in selectionStr:
                self.assertIn("usr1", selectionStr)

if __name__ == "__main__":
    unittest.main()
