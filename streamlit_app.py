
import logging
import streamlit as st
from sqlalchemy import create_engine, inspect
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set to DEBUG for more verbosity
logger = logging.getLogger(__name__)

def log_exception(e, context=""):
    logger.error(f"Error occurred during {context}: {e}", exc_info=True)
    st.error(f"An error occurred during {context}: {e}")

# Example connection setup with error logging
def get_database_connection():
    try:
        # Example connection string with SSL and logging
        engine = create_engine("postgresql://user:password@172.26.63.252:5432/postgres?sslmode=require")
        logger.info("Database connection established.")
        return engine
    except Exception as e:
        log_exception(e, "database connection")
        return None

# Function to inspect tables
def inspect_tables(engine, schema_name):
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names(schema=schema_name)
        logger.info(f"Retrieved tables from schema '{schema_name}': {tables}")
        return tables
    except Exception as e:
        log_exception(e, f"retrieving tables from schema '{schema_name}'")
        return []

# Example usage inside Streamlit app
def main():
    st.title("Database Connection Test")
    engine = get_database_connection()
    
    if engine:
        schema_name = "your_schema_name"  # Replace with your actual schema name
        tables = inspect_tables(engine, schema_name)
        
        if tables:
            st.write(f"Tables in schema '{schema_name}': {tables}")
            try:
                df = get_table_data(engine, schema_name, tables[0], limit=5)
                st.dataframe(df)
            except Exception as e:
                log_exception(e, f"fetching data from table '{tables[0]}'")
        else:
            st.warning(f"No tables found in schema '{schema_name}'.")
    else:
        st.error("Failed to connect to the database. Check logs for details.")

# Function to fetch table data
def get_table_data(engine, schema_name, table_name, limit=10):
    try:
        query = f'SELECT * FROM {schema_name}.{table_name} LIMIT {limit}'
        with engine.connect() as connection:
            data = pd.read_sql(query, connection)
        logger.info(f"Fetched data from table '{table_name}'.")
        return data
    except Exception as e:
        log_exception(e, f"fetching data from table '{table_name}'")
        return pd.DataFrame()

if __name__ == "__main__":
    main()
