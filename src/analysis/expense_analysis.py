import pandas as pd
import logging

class ExpenseAnalysis:
    def __init__(self, df):
        self.df = df
        self.logger = logging.getLogger(__name__)
    
    def sort_by_category(self):
        """
        Sorts categories with expenses on monthly basis. 

        Returns:
        - sorted_df (dataframe): DF of sorted expenses and income on monthly basis by category.
        """
        try:
            # Ensure the 'Month' column is derived from the 'Date' column
            self.df['Month'] = self.df['Date'].dt.to_period('M')

            # Group data by 'Category' and 'Month', summing the 'Amount'
            grouped_df = self.df.groupby(['Month', 'Category'])['Amount'].sum().reset_index()

            # Sort by 'Month' (ascending) and 'Amount' within each month (ascending)
            sorted_df = grouped_df.sort_values(by=['Month', 'Amount'], ascending=[True, True])
            self.logger.info("Expenses sorted by category and month:\n%s", sorted_df.to_string(index=False))
            return sorted_df
        except Exception as e:
            self.logger.error(f"Error sorting data by category and month: {e}")
            raise
        

    def monthly_summary(self):
        """
       Generates monthly summary of expenses by category by summing them over a month. 

        Returns:
        - summary (dataframe): DF of expenses by category by summing them over a month and expense to income ratio.
        """
        self.df['Month'] = self.df['Date'].dt.to_period('M')
        summary = self.df.groupby('Month').agg(
            total_income=('Amount', lambda x: x[x > 0].sum()),
            total_expenses=('Amount', lambda x: abs(x[x < 0].sum()))
        ).reset_index()
        summary['expense_to_income_ratio'] = summary['total_expenses'] / summary['total_income']
        self.logger.info("Monthly Summary of Expenses and Income:\n%s", summary.to_string(index=False))
        return summary

    def savings_recommendations(self, income_threshold=0.1, reduction_percentage=0.15):
        """
        Identifies categories with expenses higher than a specified percentage of monthly income 
        and generates recommendations for reducing these expenses.

        Parameters:
        - income_threshold (float): The allowable maximum percentage of income that can be spent on a category.
        - reduction_percentage (float): The suggested reduction percentage for categories exceeding the threshold.

        Returns:
        - recommendations (list): List of strings containing insights and recommendations.
        """
        try:
            self.df['Date'] = pd.to_datetime(self.df['Date'], errors='coerce')
            self.df['Month'] = self.df['Date'].dt.to_period('M')

            # Calculate monthly income
            monthly_income = self.df[self.df['Amount'] > 0].groupby('Month')['Amount'].sum()

            # Calculate monthly expenses per category
            monthly_expenses = self.df[self.df['Amount'] < 0].groupby(['Month', 'Category'])['Amount'].sum().abs()

            # Generate recommendations
            recommendations = []

            for month in monthly_income.index:
                income = monthly_income.get(month, 0)
                if income > 0:  # Ensure valid income exists for the month
                    for (m, category), expense in monthly_expenses.items():
                        if m == month:
                            expense_ratio = expense / income
                            if expense_ratio > income_threshold:
                                excess_percentage = round((expense_ratio - income_threshold) * 100, 2)
                                reduction_needed = round(reduction_percentage * 100, 2)
                                recommendations.append(
                                    f"In {month}, the '{category}' expenses were {excess_percentage}% over the {income_threshold * 100}% "
                                    f"threshold of monthly income. It is recommended to reduce '{category}' expenses by {reduction_needed}% "
                                    "to better meet savings goals."
                                )

            if not recommendations:
                recommendations.append("All expenses are within the desired limits for each category.")

            self.logger.info("Generated savings recommendations.")
            return recommendations

        except Exception as e:
            self.logger.error(f"Error generating savings recommendations: {e}")
            raise

    def calculate_monthly_savings_goal_reduction(self, savings_goal=500):
        """
        Calculates the proportion by which monthly expenses need to be reduced to meet a specified savings goal for each month.

        Parameters:
        - savings_goal (float): The user's monthly savings goal.

        Returns:
        - dict: A dictionary where keys are months, and values are the percentage reduction needed or a message indicating no reduction is required.
        """
        try:
            # Ensure 'Date' is a datetime type and create a 'Month' column
            self.df['Date'] = pd.to_datetime(self.df['Date'])
            self.df['Month'] = self.df['Date'].dt.to_period('M')

            # Calculate monthly income and expenses
            monthly_income = self.df[self.df['Amount'] > 0].groupby('Month')['Amount'].sum()
            monthly_expenses = self.df[self.df['Amount'] < 0].groupby('Month')['Amount'].sum().abs()

            monthly_reductions = {}

            for month in monthly_income.index:
                income = monthly_income.get(month, 0)
                if income > 0:
                    monthly_expense_after_savings = income - savings_goal
                    total_expenses = monthly_expenses.get(month, 0)

                    if total_expenses > monthly_expense_after_savings:
                        reduction_needed = ((total_expenses - monthly_expense_after_savings) / total_expenses) * 100
                        self.logger.info(f"Month {month}: Calculated reduction needed: {reduction_needed:.2f}% to meet savings goal.")
                        monthly_reductions[month] = f"A reduction of {reduction_needed:.2f}% in total expenses is needed to meet the savings goal."
                    else:
                        self.logger.info(f"Month {month}: No reduction needed; total expenses are within the savings goal.")
                        monthly_reductions[month] = "No reduction needed; expenses are already within the savings goal."
                else:
                    self.logger.info(f"Month {month}: Zero income, cannot calculate a meaningful reduction.")
                    monthly_reductions[month] = "Zero income for this month; unable to calculate expense reduction."

            return monthly_reductions

        except Exception as e:
            self.logger.error(f"Error calculating monthly savings goal reduction: {e}")
            raise



