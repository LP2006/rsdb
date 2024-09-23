import pyodbc
import pandas as pd
import streamlit as st

# Define the ODBC connection using the System-DSN
def connect_to_db():
    try:
        # Replace 'your_dsn' with the name of your System-DSN
        connection = pyodbc.connect('DSN=PostgreSQL;UID=lkp;PWD=voeko')
        st.success("Database connection established.")
        return connection
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# Fetch data from a table
def fetch_data(connection, table_name):
    try:
        query = f"SELECT * FROM {table_name} LIMIT 10"
        df = pd.read_sql(query, connection)
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

# Streamlit app layout
st.title("ODBC PostgreSQL Connection")

# Connect to the database
connection = connect_to_db()

if connection:
    # List the tables (you can use another query to list tables if needed)
    table_name = st.text_input("Enter the table name", "your_table")

    # Fetch and display the data
    if table_name:
        data = fetch_data(connection, table_name)
        if data is not None:
            st.write(data)
