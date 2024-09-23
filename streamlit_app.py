import streamlit as st
import pyodbc
import pandas as pd

# Function to connect to the PostgreSQL DB via ODBC
def connect_to_db():
    try:
        # Here, replace 'PostgreSQL' with the name of your DSN (e.g. 'PostgreSQL' from the image)
        connection = pyodbc.connect('DSN=PostgreSQL;UID=lkp;PWD=voeko')
        st.success("Database connection established successfully!")
        return connection
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# Function to fetch data from a specific table
def fetch_table_data(connection, table_name, limit=10):
    query = f"SELECT * FROM {table_name} LIMIT {limit}"
    return pd.read_sql(query, connection)

# Streamlit app layout
st.title("ODBC PostgreSQL Connection")

# Connect to the database
conn = connect_to_db()

if conn:
    table_name = st.text_input("Enter the table name to fetch data from:", "your_table_name")
    if st.button("Fetch Data"):
        df = fetch_table_data(conn, table_name)
        st.write(df)
