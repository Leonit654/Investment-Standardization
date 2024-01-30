import sqlite3
from datetime import datetime

# Database connection parameters
db_file = 'db.sqlite3'

# SQL script
sql_script = """
INSERT INTO cash_flows_cashflowtype (value, created_at, updated_at) VALUES
  ('funding', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('deposit', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('withdrawal', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('general_repayment', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('principal_repayment', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('interest_repayment', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
"""


def load_initial_data():
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)

        # Create a cursor object to execute SQL statements
        cursor = connection.cursor()

        # Execute the SQL script
        cursor.executescript(sql_script)

        # Commit the changes and close the connection
        connection.commit()
        connection.close()

        print("Data inserted successfully.")

    except Exception as e:
        print(f"Error executing SQL script: {e}")


if __name__ == "__main__":
    load_initial_data()
