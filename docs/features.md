- **Feature: Merge Columns**
  - Description: This feature allows users to merge the values of two columns into a new column using specified operators.
  - Operators: ['sum','subtract','multiply']
  - Key: merge_columns
  - Value: 
  - For each at a time:
    ```json
       [
         {
            "new_column_name": "new_column_name",
            "operator": "subtract",
            "columns_to_merge": ["column1", "column2"]
         }
       ]
    ```
  - For all in one endpoint:
      ```json
       { 
    "trade":[
          {
            "new_column_name": "new_realized",
            "operator": "subtract",
            "columns_to_merge": ["purchased_amount", "interest_rate_exp"]
          }
    
        ],
    "cash_flow":[
          {
                "new_column_name": "merged_columns",
                "operator": "subtract",
                "columns_to_merge": ["realized_amount", "realized_amount"]
          }
        ]
     
     }
    ```  