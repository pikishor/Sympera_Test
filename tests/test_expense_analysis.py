import unittest
import pandas as pd
from src.analysis.expense_analysis import ExpenseAnalysis
import logging

class TestExpenseAnalysis(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Set up logging for test output visibility
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        cls.logger = logging.getLogger(__name__)

        # Sample data for testing
        data = {
            'Date': pd.to_datetime(['2024-01-05', '2024-01-15', '2024-02-10', '2024-02-20', '2024-03-05']),
            'Category': ['Food', 'Entertainment', 'Rent', 'Food', 'Travel'],
            'Amount': [-100, -50, -800, -150, -300]
        }
        cls.df = pd.DataFrame(data)

        # Create instance of ExpenseAnalysis
        cls.expense_analysis = ExpenseAnalysis(cls.df)

    def test_sort_by_category(self):
        sorted_df = self.expense_analysis.sort_by_category()
        self.assertFalse(sorted_df.empty, "The sorted DataFrame should not be empty.")
        self.logger.info("Sort by category test passed.")

    def test_monthly_summary(self):
        summary = self.expense_analysis.monthly_summary()
        self.assertIn('total_income', summary.columns, "Summary DataFrame should contain 'total_income' column.")
        self.assertIn('total_expenses', summary.columns, "Summary DataFrame should contain 'total_expenses' column.")
        self.logger.info("Monthly summary test passed.")

    def test_savings_recommendations(self):
        recommendations = self.expense_analysis.savings_recommendations(income_threshold=0.1, reduction_percentage=0.15)
        self.assertIsInstance(recommendations, list, "Recommendations should be a list.")
        self.logger.info("Savings recommendations test passed.")

    def test_calculate_monthly_savings_goal_reduction(self):
        monthly_reductions = self.expense_analysis.calculate_monthly_savings_goal_reduction(savings_goal=500)
        self.assertIsInstance(monthly_reductions, dict, "Monthly reductions should be a dictionary.")
        for month, message in monthly_reductions.items():
            self.assertIsInstance(message, str, "Each value in the monthly reductions dictionary should be a string.")
        self.logger.info("Calculate monthly savings goal reduction test passed.")

if __name__ == "__main__":
    unittest.main()
