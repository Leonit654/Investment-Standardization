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




- **Key: values_to_replace**
  - **Value:**
    ```json
    [
      {
          "column_name": "cash_flow_type",
          "operator": "&",
          "value": "withdrawal",
          "condition": [
              {"column_name": "cash_flow_type", "operator": "==", "value": "'cash_order'"},
              {"column_name": "amount", "operator": "<", "value": 0}
          ]
      },
      {
          "column_name": "cash_flow_type",
          "operator": "&",
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

- **Key: values_to_replace**
  - **Value:**
    ```json
    [
        {
        "column_name": "cash_flow_type",
        "value": "general_repayment",
        "operator":"|",
        "condition": [
            {"column_name": "cash_flow_type", "operator": "==", "value": "'repayment'"}
                    ]
         }
    ]
    ```

## SME Finance Data:

### Method: POST
### URL: http://127.0.0.1:8000/trades/synchronize/all-in-one/

#### Request Body (form-data):
- **Key: file**
  - **Value:** Your cashflow file

- **Key: file_title**
  - **Value:** Your file title

- **Key: column_mapping**
  - **Value:**
    ```json
      {
    "trade": {
      "asset_id": "identifier",
      "issue_date": "issue_date",
      "maturity_date": "maturity_date",
      "purchased_amount": "invested_amount",
      "interest_rate_exp": "interest_rate"
     },
    "cash_flow": {
      "cash_flow_type": "cash_flow_type",
      "cashflow_date": "date",
      "realized_amount": "amount",
      "asset_id": "trade_identifier",
      "cashflow_id": "identifier"
        }
    }
    ```

- **Key: values_to_replace**
  - **Value:**
    ```json
    [
          {
              "column_name": "cash_flow_type",
              "value": "principal_repayment",
              "operator":"|",
              "condition": [
                  {"column_name": "cash_flow_type", "operator": "==", "value": "'Principal Repayment'"},
                  {"column_name": "cash_flow_type", "operator": "==", "value": "'Principal repayment'"},
                  {"column_name": "cash_flow_type", "operator": "==", "value": "'Commission Repayment'"},
                  {"column_name": "cash_flow_type", "operator": "==", "value": "'repayment_adjustment'"}
              ]
          },
          {
              "column_name": "cash_flow_type",
              "value": "funding",
              "operator":"|",
              "condition": [
                  {"column_name": "cash_flow_type", "operator": "==", "value": "'Funding'"}
              ]
          },
             {
              "column_name": "cash_flow_type",
              "value": "interest_repayment",
              "operator":"|",
              "condition": [
                  {"column_name": "cash_flow_type", "operator": "==", "value": "'Interest Repayment'"},
                  {"column_name": "cash_flow_type", "operator": "==", "value": "'Interest Repayment Adjustment'"},
                  {"column_name": "cash_flow_type", "operator": "==", "value": "'other_cost'"}
              ]
          }
      ]
    ```
- **Key: sheet_mapping**
  - **Value:**
    ```json
      {
    "asset": "trade",
    "cashflow": "cash_flow"
    }
    ```
