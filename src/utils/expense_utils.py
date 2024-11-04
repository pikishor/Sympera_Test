import pandas as pd
import logging


class TransactionDataLoader:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def load_transaction_data(self, file_path):
        """
        Loads transaction data from a CSV file and converts the 'Date' column to datetime format.

        Parameters:
            file_path (str): The path to the CSV file containing transaction data.

        Returns:
            DataFrame: A pandas DataFrame containing the loaded transaction data, 
                        with the 'Date' column converted to datetime format.
        """
        try:
            df = pd.read_csv(file_path)
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            self.logger.info("Transaction data loaded successfully.")
            return df
        except Exception as e:
            self.logger.error(f"Error loading transaction data: {e}")
            raise
