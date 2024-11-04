About The Project:
    Development Challenge: "Smart Financial Management with Python"
    Task Description: Develop a Python application that allows users to analyze their expenses and income simply and gain insights into their spending habits. The system will also provide savings recommendations and guide the user toward a budget balance.

Built With:
    Python 3.10+

Installation:

    Create a virtual environment:
    python -m venv myenv

    Activate the virtual environment:
    source myenv/bin/activate


    Install libraries:
    Pip install pandas
    pip install matplotlib
    Pip install plotly
    pip install fpdf
    pip install pytest

    Data Folder:  to contain Data files. Two files are there for testing which can be renamed in main.py where path is mentioned. One file transactions_example.csv contains the orognal data whereas transactions_example copy.csv contains sample data for few more months. 

To run the code:
    python src/main.py

To run the test cases:
    python -m unittest discover -s tests -p "*.py"
    or
    python -m unittest discover -s tests -v
    or 
    for individual test files e.g. test_exchange_rate_utils:  
    PYTHONPATH=./src python -m unittest tests/test_exchange_rate_utils.py 

Logs: 
    logs folder: app.log

To clone the repository:
    git clone https://github.com/pikishor/Sympera_Test.git

