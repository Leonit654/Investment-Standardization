import sqlite3

# Database connection parameters
db_file = 'db.sqlite3'

# SQL script
sql_script = """
INSERT INTO cash_flows_cashflowtype (value, created_at, updated_at)
VALUES
  ('funding', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('deposit', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('withdrawal', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('general_repayment', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('principal_repayment', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('interest_repayment', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
"""

def check_data_exist():
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()

        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM cash_flows_cashflowtype")
        count = cursor.fetchone()[0]

        connection.close()
        return count > 0

    except Exception as e:
        print(f"Error checking data existence: {e}")
        return False

def load_initial_data():
    try:
        # Check if data already exists
        if not check_data_exist():
            # If data doesn't exist, proceed with inserting
            connection = sqlite3.connect(db_file)
            cursor = connection.cursor()

            # Execute the SQL script
            cursor.executescript(sql_script)

            # Commit the changes and close the connection
            connection.commit()
            connection.close()

            print("Data inserted successfully.")
        else:
            print("Data already exists in the database. Skipping insertion.")

    except Exception as e:
        print(f"Error executing SQL script: {e}")

if __name__ == "__main__":
    load_initial_data()
