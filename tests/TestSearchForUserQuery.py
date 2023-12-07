import unittest
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter

class TestSearchForUserQuery(unittest.TestCase):
    def setUp(self):
        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.connection_patch = patch('modules.Tweeter.sqlite3.connect', return_value=self.mock_connection)
        self.connection_patch.start()

        self.tweeter_instance = Tweeter("test.db")

    def tearDown(self):
        self.connection_patch.stop()

    def test_search_for_user_query(self):
        # Arrange
        keyword = "testuser"
        offset = 0
        # Adjust the fake_users list to include duplicates if that's the intended behavior
        fake_users = [
            (1, "TestUser1", "City1", "testuser1@example.com", 1.0)
        ]
        self.mock_cursor.fetchall.return_value = fake_users

        # Act
        result = self.tweeter_instance.search_for_user_query(keyword, offset)
        # Assert
        self.assertEqual(result[0], fake_users[0])

if __name__ == '__main__':
    unittest.main()
