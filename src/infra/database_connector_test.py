from unittest.mock import patch, MagicMock
from .database_connector import DatabaseConnection

def test_connect():
    with patch('mysql.connector.connect') as mock_connect:
        mock_connect.return_value = MagicMock()
        assert DatabaseConnection.connection is None
        DatabaseConnection.connect()
        assert DatabaseConnection.connection is not None
        mock_connect.assert_called_once()
