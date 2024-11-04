import unittest
import pandas as pd
from unittest.mock import patch, mock_open
from src.utils.expense_utils import TransactionDataLoader

class TestTransactionDataLoader(unittest.TestCase):
    @patch('pandas.read_csv')
    @patch('logging.getLogger')
    def test_load_transaction_data_success(self, mock_get_logger, mock_read_csv):
        # Create a mock DataFrame to return from read_csv
        mock_data = {
            'Date': ['2024-01-01', '2024-01-02'],
            'Amount': [1000, -500],
            'Category': ['Salary', 'Groceries']
        }
        mock_df = pd.DataFrame(mock_data)
        mock_read_csv.return_value = mock_df

        # Instantiate the TransactionDataLoader class
        transaction_loader = TransactionDataLoader()
        
        # Call the method with a fake file path
        df = transaction_loader.load_transaction_data('fake_path.csv')

        # Assertions to ensure the DataFrame is as expected
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)  # Check that two rows were loaded
        self.assertTrue(pd.to_datetime(df['Date']).notnull().all())  # Check that all dates are valid

        # Ensure that logger's info method was called
        mock_logger = mock_get_logger.return_value
        mock_logger.info.assert_called_with("Transaction data loaded successfully.")

    @patch('pandas.read_csv')
    @patch('logging.getLogger')
    def test_load_transaction_data_failure(self, mock_get_logger, mock_read_csv):
        # Simulate a failure in loading CSV
        mock_read_csv.side_effect = FileNotFoundError("File not found.")

        # Instantiate the TransactionDataLoader class
        transaction_loader = TransactionDataLoader()
        
        with self.assertRaises(FileNotFoundError):
            transaction_loader.load_transaction_data('fake_path.csv')

        # Ensure that logger's error method was called
        mock_logger = mock_get_logger.return_value
        mock_logger.error.assert_called_with("Error loading transaction data: File not found.")

if __name__ == '__main__':
    unittest.main()
