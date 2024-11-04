from src.utils.expense_utils import TransactionDataLoader
from src.utils.exchange_rate_utils import ExchangeRate
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

    # Creating instance of ExchangeRate in case of using it later. Here in CSV no currency is given so not implemented for now. 
    exchange_rate_service = ExchangeRate()
    from_currency = 'EUR'  
    to_currency = 'USD'
    try:
        rate = exchange_rate_service.get_exchange_rate(from_currency, to_currency)
        if rate is not None:
            logger.info(f"The exchange rate from {from_currency} to {to_currency} is: {rate}")
        else:
            logger.info("Failed to retrieve the exchange rate.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    # Psss the rate in the currency to implement the method
    # Or multiplyamount by rate in pandas dataframe to convert the currency from_currency to to_currency or similarly in savings.
