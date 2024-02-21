# Synchronize Trades and Cashflows

This guide provides steps to synchronize trade and cashflow data using the provided methods.
## Steps to set up and run the project using Docker

- **Setup:**
  - Use Git Bash or any terminal and run the command: 
    ```
    git clone https://github.com/Leonit654/Investment-Standardization.git
    ```

- **Running the project:**
  - After cloning the project, use PyCharm, Visual Studio Code, or any editor that supports Python programming. 
    After opening the project, open any terminal and run the command: 
    ```
    docker-compose up
    ```

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

- **Configuring Celery:**
  - Firstly install a Message Broker: 

      [Redis](https://redis.io/docs/install/install-redis/),
      [RabbitMQ](https://www.rabbitmq.com/download.html)
  - after installation, you need to start the server
      RabbitMQ
           windows: it should start automatically 
           linux: sudo systemctl status rabbitmq-server
      Redis
           windows: Run redis-server.exe to start the Redis server.
           linux: sudo systemctl status redis
  - after the server has started you need to configure your settings:
      RabbitMQ
          ` CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
           CELERY_RESULT_BACKEND = 'rpc'`
      Redis
          `CELERY_BROKER_URL = 'redis://localhost:6379/0'  
            CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'`
  - finally start the celery work:
        `celery -A Investment_Management worker -l INFO --pool=solo`


  

  

# Synchronize Trades 

## Qkuk Data:

### Method: POST
### URL: http://127.0.0.1:8000/synchronize/

#### Request Body (form-data):
- **Key: file**
  - **Value:** Your trade file

- **Key: file_title**
  - **Value:** Your file title

- **Key: merge_columns
  - **Value:**
    ```json
    [
     {
        "new_column_name": "purchase_amount",
        "operator": "sum",
        "columns_to_merge": ["total_invested_amount", "fee_amount"]
     }
    ]
    ```
- **Key: column_mapping**
  - **Value:** 
    ```json
    {
    "trade": {
        "loan_id": "identifier",
        "issue_date": "issue_date",
        "maturity_date": "maturity_date",
        "purchase_amount": "invested_amount",
        "interest_rate_exp": "interest_rate"
         },
    "cash_flow": {}
    }
    ```
- **Key: file_mapping**
  - **Value:** 
    ```json
    {
    "your_file_name.extension": "trade"
    }
    ```    

## Skurs Data:

### Method: POST
### URL: http://127.0.0.1:8000/synchronize/

#### Request Body (form-data):
- **Key: file**
  - **Value:** Your trade file

- **Key: file_title**
  - **Value:** Your file title

- **Key: column_mapping**
  - **Value:** 
    ```json
    {
        "trade":{
    "trade_id": "identifier",
    "trade_receivable_date": "issue_date",
    "due_date": "maturity_date",
    "trade_receivable_amount": "invested_amount",
    "interest_rate_exp": "interest_rate"
        },
    "cash_flow":{}
    }
    ```
- **Key: file_mapping**
  - **Value:** 
    ```json
    {
    "your_file_name.extension": "trade"
    }
    ```        


# Synchronize Cashflows

## Qkuk Data:

### Method: POST
### URL: http://127.0.0.1:8000/synchronize/

#### Request Body (form-data):
- **Key: file**
  - **Value:** Your cashflow file

- **Key: file_title**
  - **Value:** Your file title

- **Key: column_mapping**
- **Value:**
  ```json
  {
      "trade": [],
      "cash_flow": {
          "cashflow_type": "cash_flow_type",
          "cashflow_date": "date",
          "amount": "amount",
          "loan_identifier": "trade_identifier",
          "identifier": "identifier"
      }
  }
  ```
- **Key: values_to_replace**
  - **Value:**
    ```json
    {
      "trade": [],
      "cash_flow": [
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
    }
    ```
- **Key: file_mapping**
  - **Value:** 
    ```json
    {
    "your_file_name.extension": "cash_flow"
    }
    ```      

## Skurs Data:

### Method: POST
### URL: http://127.0.0.1:8000/synchronize/

#### Request Body (form-data):
- **Key: file**
  - **Value:** Your cashflow file

- **Key: file_title**
  - **Value:** Your file title

- **Key: column_mapping**
  - **Value:**
    ```json
    {
    "trade":{},
      "cash_flow":{
      "cashflow_type": "cash_flow_type",
      "cashflow_date": "date",
      "amount": "amount",
      "trade_id": "trade_identifier",
      "cashflow_id": "identifier"
      }
    }
    ```

- **Key: values_to_replace**
  - **Value:**
    ```json
    {
    "trade":{},
      "cash_flow":[
      {
          "column_name": "cash_flow_type",
          "value": "general_repayment",
          "operator":"|",
          "condition": [
              {"column_name": "cash_flow_type", "operator": "==", "value": "'repayment'"}
              
          ]
      }
      
      ]
    }
    ```
- **Key: file_mapping**
  - **Value:** 
    ```json
    {
    "your_file_name.extension": "cash_flow"
    }
    ```          


## SME Finance Data:

### Method: POST
### URL: http://127.0.0.1:8000/synchronize/

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
    {
    "trade": {},
    "cash_flow": [
        {
            "column_name": "cash_flow_type",
            "value": "principal_repayment",
            "operator": "|",
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
            "operator": "|",
            "condition": [
                {"column_name": "cash_flow_type", "operator": "==", "value": "'Funding'"}
            ]
        },
        {
            "column_name": "cash_flow_type",
            "value": "interest_repayment",
            "operator": "|",
            "condition": [
                {"column_name": "cash_flow_type", "operator": "==", "value": "'Interest Repayment'"},
                {"column_name": "cash_flow_type", "operator": "==", "value": "'Interest Repayment Adjustment'"},
                {"column_name": "cash_flow_type", "operator": "==", "value": "'other_cost'"}
            ]
        }
    ]
    }
    ```
- **Key: sheet_mapping**
  - **Value:**
    ```json
      {
    "asset": "trade",
    "cashflow": "cash_flow"
    }
    ```
    
# Trade Details:
  **Method: GET, PUT, DELETE**

  **URL: http://127.0.0.1:8000/trades/trade-details/<str:identifier>/**

# Cash Flows Details:
  **Method: GET, PUT, DELETE**

  **URL: http://127.0.0.1:8000/cash_flows/cash_flow_detail/<str:identifier>/**

### Get all Cash Flows:
  **Method: GET**

  **URL:http://127.0.0.1:8000/cash_flows/list_cash_flows/**

# Cash Flow Types Details:
  **Method: GET, PUT, DELETE**

  **URL: http://127.0.0.1:8000/cash_flows/cash_flow_type_detail/<str:value>/**


### Get all Cash Flow Types:
  **Method: GET**

  **URL:http://127.0.0.1:8000/cash_flows/list_cash_flow_type/**

### Add a Cash Flow Type: 

**Method: POST**

**URL : http://127.0.0.1:8000/cash_flows/list_cash_flow_type/**
#### Request Body (form-data):
- **Key: value**
  - **Value:** Your cashflow type file

    
# **Trade Formulas:**

    Trade identifier to test: 3366

##   Realized Amount Endpoint
  
    URL: http://localhost:8000/trades/realized_amount/<identifier>/
    Method: POST
    Description: Retrieves the realized amount for a trade.
    Parameters:
      identifier: Identifier of the trade.
      reference_date: Date for reference. Default is '2023-12-04'.

      POST /realized_amount/123456/
      Body: {"reference_date": "2024-01-01"}
  
  
##   Gross Expected Amount Endpoint
  
    URL: http://localhost:8000/trades/gross_expected_amount/<identifier>/
    Method: POST
    Description: Retrieves the gross expected amount for a trade.
    Parameters:
      identifier: Identifier of the trade.
      reference_date: Date for reference. Default is '2023-12-04'.
      
      POST /gross_expected_amount/123456/
      Body: {"reference_date": "2024-01-01"}
  
  
##   Remaining Invested Amount Endpoint
  
    URL: http://localhost:8000/trades/remaining_invested_amount/<identifier>/
    Method: POST
    Description: Retrieves the remaining invested amount for a trade.
    Parameters:
      identifier: Identifier of the trade.
      reference_date: Date for reference. Default is '2023-12-04'.
      
      POST /remaining_invested_amount/123456/
      Body: {"reference_date": "2024-01-01"}
  
  
##   Closing Date Endpoint
  
    URL: http://localhost:8000/trades/closing_date/<identifier>/
    Method: GET
    Description: Retrieves the closing date for a trade.
    Parameters:
      identifier: Identifier of the trade.
      
      GET /closing_date/123456/
