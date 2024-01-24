# Synchronize Trades and Cashflows

This guide provides steps to synchronize trade and cashflow data using the provided methods.

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
