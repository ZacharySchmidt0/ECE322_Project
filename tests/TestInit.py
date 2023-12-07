import unittest
from unittest.mock import patch, MagicMock
from modules.Tweeter import Tweeter


class TestTweeterInit(unittest.TestCase):
    @patch('modules.Tweeter.sqlite3')  
    def test_init(self, mock_sqlite):
        mock_connection = MagicMock()
        mock_sqlite.connect.return_value = mock_connection
        target_db = "test.db"
        tweeter_instance = Tweeter(target_db)
        mock_sqlite.connect.assert_called_with(target_db)
        self.assertEqual(tweeter_instance.conn, mock_connection)
        self.assertIsNotNone(tweeter_instance.c)


if __name__ == '__main__':
    unittest.main()
