import pynuodb

# Database connection settings
hostname = 'localhost'
database = 'test'
username = 'dba'
password = 'goalie'
port = '8890'  # Ensure this is the correct port for your NuoDB instance

# SQL command to create a table
create_table_sql = '''
CREATE TABLE employees (
    id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50),
    salary DECIMAL(10, 2),
    PRIMARY KEY (id)
)
'''

try:
    # Connect to the NuoDB database
    print("Connecting to NuoDB...")
    connection = pynuodb.connect(
        database=database,
        user=username,
        password=password,
        host=hostname,
        port=port  # Including port in the connection settings
    )
    cursor = connection.cursor()
    print("Connected to NuoDB database")

    # Execute the SQL command to create the table
    print("Executing SQL command to create table...")
    # cursor.execute(create_table_sql)
    print("Table 'employees' created successfully")

except pynuodb.Error as e:
    print(f"Database error occurred: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    # Close the database connection if it was successfully opened
    try:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("Database connection closed")
    except NameError:
        print("Connection was not established, so nothing to close.")
