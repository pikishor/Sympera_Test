from fpdf import FPDF
import logging
import matplotlib.pyplot as plt

class ReportGenerator:
    def __init__(self):
        self.pdf = FPDF()
        self.logger = logging.getLogger(__name__)

    def generate_pdf_report(self, summary_df, recommendations, monthly_reductions, file_name="financial_report.pdf"):
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.add_page()
        self.pdf.set_font("Arial", "B", 16)
        self.pdf.cell(0, 10, "Financial Report", ln=True, align="C")

        self.pdf.set_font("Arial", size=12)
        self.pdf.ln(10)
        for _, row in summary_df.iterrows():
            self.pdf.cell(0, 10, f"{row['Month']}: Income: {row['total_income']:.2f}, Expenses: {row['total_expenses']:.2f}", ln=True)

        self.pdf.ln(10)
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.cell(0, 10, "Recommendations:", ln=True)
        self.pdf.set_font("Arial", size=12)
        for rec in recommendations:
            self.pdf.multi_cell(0, 10, rec)

        # Add Monthly Savings Goal Reductions
        self.pdf.ln(10)
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.cell(0, 10, "Monthly Savings Goal Reductions:", ln=True)
        self.pdf.set_font("Arial", size=12)
        for month, message in monthly_reductions.items():
            self.pdf.cell(0, 10, f"{month}: {message}", ln=True)

        # Generate and save the graph
        self.generate_graph_image(summary_df)

        # Add the graph to the PDF
        self.pdf.add_page()  # Add a new page for the graph
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.cell(0, 10, "Monthly Income vs Expenses Graph", ln=True)
        self.pdf.ln(5)
        self.pdf.image("monthly_expenses_vs_income.png", x=10, y=None, w=180)

        self.pdf.output(file_name)
        self.logger.info(f"PDF report generated: {file_name}")

    def generate_graph_image(self, summary_df):
        plt.figure(figsize=(10, 6))
        plt.plot(summary_df['Month'].astype(str), summary_df['total_income'], label='Income', marker='o')
        plt.plot(summary_df['Month'].astype(str), summary_df['total_expenses'], label='Expenses', marker='o')
        plt.title('Monthly Income vs Expenses')
        plt.xlabel('Month')
        plt.ylabel('Amount')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.savefig("monthly_expenses_vs_income.png")
        plt.close()
