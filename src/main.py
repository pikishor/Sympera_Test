from src.utils.expense_utils import TransactionDataLoader
from src.analysis.expense_analysis import ExpenseAnalysis
from src.visualizations.expense_visualization import ExpenseVisualization
from reports.expense_report import ReportGenerator
import logging


# Set up global logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='logs/app.log',
    filemode='a'  # Append to existing log file
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Application started")
    file_path = "data/transactions_example copy.csv"  # Replace with your actual CSV file path
    transaction_data = TransactionDataLoader()
    transactions_df = transaction_data.load_transaction_data(file_path)

    expense_analysis = ExpenseAnalysis(transactions_df)
    sorted_df = expense_analysis.sort_by_category()
    monthly_summary_df = expense_analysis.monthly_summary()
    recommendations = expense_analysis.savings_recommendations()
    logger.info("\nRecommendations:")
    for rec in recommendations:
        logger.info(rec)

    savings_goal = float(input("Enter your monthly savings goal: "))
    monthly_reductions = expense_analysis.calculate_monthly_savings_goal_reduction(savings_goal)
    for month, message in monthly_reductions.items():
        print(f"{month}: {message}")
        logger.info("\nGoal Recommendation:")
        logger.info(f"{month}: {message}")

    expense_visualization = ExpenseVisualization(transactions_df)
    expense_visualization.plot_expenses_vs_income()
    expense_report_generator = ReportGenerator()
    expense_report_generator.generate_pdf_report(monthly_summary_df, recommendations, monthly_reductions)
