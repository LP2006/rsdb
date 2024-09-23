import streamlit as st
import pyodbc

# Function to establish a connection to the PostgreSQL database
@st.cache_resource
def connect_to_db():
    try:
        # Connection string using the correct ODBC driver
        conn_str = (
            "DRIVER={PostgreSQL ODBC Driver(UNICODE)};"
            "SERVER=172.26.63.252;"
            "PORT=5432;"
            "DATABASE=postgres;"  
            "UID=lkp;"      
            "PWD=voeko;"      
        )

        # Establish the connection
        conn = pyodbc.connect(conn_str)
        st.success("Connection successful!")
        return conn

    except pyodbc.Error as e:
        st.error(f"Error connecting to database: {e}")
        return None

# Streamlit app layout
st.title("PostgreSQL ODBC Connection in Streamlit")

# Button to trigger connection attempt
if st.button("Connect to Database"):
    conn = connect_to_db()
    
    if conn:
        # Example of querying the database if connection is successful
        query = "SELECT version();"
        cursor = conn.cursor()
        cursor.execute(query)
        version = cursor.fetchone()
        st.write(f"PostgreSQL version: {version[0]}")
        cursor.close()
        conn.close()
