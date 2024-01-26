# Synchronize Trades and Cashflows

This guide provides steps to synchronize trade and cashflow data using the provided methods.

## Steps to set up and run the project

- **Setup:**
  - Use Git Bash or any terminal and run the command: 
    ```
    git clone https://github.com/Leonit654/Investment-Standardization.git
    ```

- **Creating virtual environment:**
  - After cloning the project, use PyCharm, Visual Studio Code, or any editor that supports Python programming. 
    After opening the project, open any terminal and run the command: 
    ```
    python -m venv venv
    ```

- **Activating virtual environment:**
  - for Windows users: 
    ```
    venv/Scripts/activate
    ```
  - for Linux users: 
    ```
    source activate
    ```

- **Installing required libraries:**
  - After activating venv, use the command 
    ```
    pip install -r requirements.txt
    ``` 
    to install required libraries.

- **Migrate database:**
  - Use commands 
    ```
    python manage.py makemigrations
    ```
    and 
    ```
    python manage.py migrate
    ```
    to define tables of the database.

- **Inserting standard data:**
  - To insert the standard data, use the command: 
    ```
    python execute_sql_script.py
    ```

- **Running the project:**
  - To run the project, use the command: 
    ```
    python manage.py runserver
    ```
    and you should be able to use the project.

## Synchronize Trades (Qkuk Data)

### Method: POST
### URL: http://127.0.0.1:8000/trades/synchronize/

#### Request Body (form-data):
- **Key: file**
  - **Value:** Your trade file

- **Key: column_mapping**
  - **Value:** 
    ```json
    {
        "identifier": "loan_id",
        "issue_date": "issue_date",
        "maturity_date": "maturity_date",
        "invested_amount": "purchase_amount",
        "interest_rate": "interest_rate_exp"
    }
    ```

## Synchronize Cashflows(Qkuk data)

### Method: POST
### URL: http://127.0.0.1:8000/cash_flows/synchronize/

#### Request Body (form-data):
- **Key: file**
  - **Value:** Your cashflow file

- **Key: column_mapping**
  - **Value:**
    ```json
    {
        "cash_flow_type": "cashflow_type",
        "date": "cashflow_date",
        "amount": "amount",
        "trade_identifier": "loan_identifier",
        "identifier": "identifier"
    }
    ```

- **Key: cash_flow_type_mapping**
  - **Value:**
    ```json
    {
        "funding": "funding",
        "principal_repayment": "principal_repayment",
        "interest_repayment": "interest_repayment",
        "cash_order": "cash_order"
    }
    ```
