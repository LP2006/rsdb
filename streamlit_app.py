
import pandas as pd
from sqlalchemy import create_engine, inspect
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define your schema name
schema_name = 'rsdb'

# Create SQLAlchemy engine
#engine = create_engine('postgresql://lkp:voeko@172.26.63.252:5432/postgres')
engine = create_engine("postgresql://lkp:voeko@172.26.63.252:5432/postgres", pool_pre_ping=True)

# Function to get tables in the schema
def get_tables():
    inspector = inspect(engine)
    tables = inspector.get_table_names(schema=schema_name)
    return tables

# Function to get table data
def get_table_data(table_name, limit=10, offset=0, search=''):
    query = f'''
        SELECT * FROM {schema_name}.{table_name}
        WHERE column_name ILIKE '%{search}%'
        LIMIT {limit} OFFSET {offset}
    '''
    with engine.connect() as connection:
        data = pd.read_sql(query, connection)
    return data

# Example usage
tables = get_tables()
print("Tables in schema:", tables)

if tables:
    df = get_table_data(tables[0], limit=5)
    print(df)
