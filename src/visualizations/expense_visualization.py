import matplotlib.pyplot as plt
import logging

class ExpenseVisualization:
    def __init__(self, df):
        self.df = df
        self.logger = logging.getLogger(__name__)

    def plot_expenses_vs_income(self):
        self.df['Month'] = self.df['Date'].dt.to_period('M')
        monthly_data = self.df.groupby('Month').agg(
            total_income=('Amount', lambda x: x[x > 0].sum()),
            total_expenses=('Amount', lambda x: abs(x[x < 0].sum()))
        ).reset_index()

        plt.figure(figsize=(10, 6))
        plt.plot(monthly_data['Month'].astype(str), monthly_data['total_income'], label='Income', marker='o')
        plt.plot(monthly_data['Month'].astype(str), monthly_data['total_expenses'], label='Expenses', marker='o')
        plt.title('Monthly Income vs Expenses')
        plt.xlabel('Month')
        plt.ylabel('Amount')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
