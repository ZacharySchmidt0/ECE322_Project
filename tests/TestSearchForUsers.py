import unittest
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter

class TestSearchForUsers(unittest.TestCase):
    def setUp(self):
        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.connection_patch = patch('modules.Tweeter.sqlite3.connect', return_value=self.mock_connection)
        self.connection_patch.start()

        self.tweeter_instance = Tweeter("test.db")

    def tearDown(self):
        self.connection_patch.stop()
        
    @patch('modules.Tweeter.inquirer.text')
    @patch('modules.Tweeter.inquirer.select')
    def test_search_for_users(self, mock_select, mock_text):
        # Arrange: Simulate user input 'x' to exit the search_for_users method
        mock_select.return_value.execute.side_effect = ['x', 'Exit']  # 'Exit' or appropriate value for the second call

        # Act: Call the search_for_users method
        self.tweeter_instance.search_for_users()

        # Assert: Check if inquirer.select was called
        self.assertEqual(mock_select.return_value.execute.call_count, 2)

if __name__ == '__main__':
    unittest.main()
