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
    python load_initial_data.py
    ```

- **Running the project:**
  - To run the project, use the command: 
    ```
    python manage.py runserver
    ```
    and you should be able to use the project.

# Synchronize Trades 

## Qkuk Data:

### Method: POST
### URL: http://127.0.0.1:8000/trades/synchronize/

#### Request Body (form-data):
- **Key: file**
  - **Value:** Your trade file

- **Key: file_title**
  - **Value:** Your file title

- **Key: column_mapping**
  - **Value:** 
    ```json
    {
    "loan_id": "identifier",
    "issue_date": "issue_date",
    "maturity_date": "maturity_date",
    "purchase_amount": "invested_amount",
    "interest_rate_exp": "interest_rate"
    }
    ```
## Skurs Data:

### Method: POST
### URL: http://127.0.0.1:8000/trades/synchronize/

#### Request Body (form-data):
- **Key: file**
  - **Value:** Your trade file

- **Key: file_title**
  - **Value:** Your file title

- **Key: column_mapping**
  - **Value:** 
    ```json
    {
    "trade_id": "identifier",
    "trade_receivable_date": "issue_date",
    "due_date": "maturity_date",
    " trade_receivable_amount ": "invested_amount",
    "interest_rate_exp": "interest_rate"
    }
    ```

# Synchronize Cashflows

## Qkuk Data:

### Method: POST
### URL: http://127.0.0.1:8000/cash_flows/synchronize/

#### Request Body (form-data):
- **Key: file**
  - **Value:** Your cashflow file

- **Key: file_title**
  - **Value:** Your file title

- **Key: column_mapping**
  - **Value:**
    ```json
    {
    "cashflow_type": "cash_flow_type",
    "cashflow_date": "date",
    "amount": "amount",
    "loan_identifier": "trade_identifier",
    "identifier": "identifier"
    }
    ```

# TODO: Remove this =========================
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
# ============================================

# TODO: Add operator
- **Key: values_to_replace**
  - **Value:**
    ```json
    [
      {
          "column_name": "cash_flow_type",
          "value": "withdrawal",
          "condition": [
              {"column_name": "cash_flow_type", "operator": "==", "value": "'cash_order'"},
              {"column_name": "amount", "operator": "<", "value": 0}
          ]
      },
      {
          "column_name": "cash_flow_type",
          "value": "deposit",
          "condition": [
              {"column_name": "cash_flow_type", "operator": "==", "value": "'cash_order'"},
              {"column_name": "amount", "operator": ">", "value": 0}
          ]
      }
    ]
    ```
## Skurs Data:

### Method: POST
### URL: http://127.0.0.1:8000/cash_flows/synchronize/

#### Request Body (form-data):
- **Key: file**
  - **Value:** Your cashflow file

- **Key: file_title**
  - **Value:** Your file title

- **Key: column_mapping**
  - **Value:**
    ```json
    {
    "cashflow_type": "cash_flow_type",
    "cashflow_date": "date",
    "amount": "amount",
    "trade_id": "trade_identifier",
    "cashflow_id": "identifier"
    }
    ```

- **Key: cash_flow_type_mapping**
  - **Value:**
    ```json
    {
    "funding": "funding",
    "principal_repayment": "principal_repayment",
    "interest_repayment": "interest_repayment",
    "deposit":"deposit",
    "withdrawal":"withdrawal"
    }
    ```

- **Feature: Merge Columns**
  - Description: This feature allows users to merge the values of two columns into a new column using specified operators.
  - Operators: ['sum','subtract','multiply']
  - Key: merge_columns
  - Value: 
    ```json
       [
         {
            "new_column_name": "new_column_name",
            "operator": "subtract",
            "columns_to_merge": ["column1", "column2"]
         }
       ]
    ```


# TODO: Add instructions to synchronize multi_sheet data (sme-finance)
# Beautify function or method creation or call, if all parameters (or arguments) fit in one line, you leave it in on
#    line. Otherwise, you put one parameter (argument) per line