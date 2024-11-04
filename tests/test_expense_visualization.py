import unittest
import pandas as pd
import matplotlib.pyplot as plt
from unittest.mock import patch
from src.visualizations.expense_visualization import ExpenseVisualization  # Adjust import based on your module structure

class TestExpenseVisualization(unittest.TestCase):
    @patch('matplotlib.pyplot.show')
    def test_plot_expenses_vs_income(self, mock_show):
        # Create a sample DataFrame for testing
        data = {
            'Date': pd.date_range(start='2024-01-01', periods=10, freq='M'),
            'Amount': [1000, -500, 1200, -600, 1300, -700, 1500, -800, 1400, -750]
        }
        df = pd.DataFrame(data)

        # Instantiate the ExpenseVisualization class
        expense_viz = ExpenseVisualization(df)

        # Run the plot method to ensure it executes without error
        try:
            expense_viz.plot_expenses_vs_income()
            self.assertTrue(True)  # If it reaches this point, the test passes
        except Exception as e:
            self.fail(f"plot_expenses_vs_income() raised an exception: {e}")

        # Verify that plt.show() was called
        mock_show.assert_called_once()

if __name__ == '__main__':
    unittest.main()
