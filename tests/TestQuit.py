import unittest
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter

class TestTweeterQuit(unittest.TestCase):
    def setUp(self):
        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.connection_patch = patch('modules.Tweeter.sqlite3.connect', return_value=self.mock_connection)
        self.connection_patch.start()

    def tearDown(self):
        self.connection_patch.stop()

    def test_quit(self):
        tweeter_instance = Tweeter("test.db")
        with self.assertRaises(SystemExit):
            tweeter_instance.quit()

if __name__ == '__main__':
    unittest.main()
