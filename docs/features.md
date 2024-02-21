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
