
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


# Fetch tables from the specified schema
try:
    inspector = inspect(engine)
    tables = inspector.get_table_names(schema=schema_name)
    print(f"Tables in schema '{schema_name}':", tables)
except Exception as e:
    print(f"Error retrieving tables: {e}")

# Function to get table data
def get_table_data(table_name, limit=10, offset=0, search='', column_name='your_column_here'):
    query = f'''
        SELECT * FROM {schema_name}.{table_name}
        WHERE {column_name} ILIKE %s
        LIMIT %s OFFSET %s
    '''
    with engine.connect() as connection:
        data = pd.read_sql(query, connection, params=[f'%{search}%', limit, offset])
    return data

# Fetch data from the first table
if tables:
    try:
        df = get_table_data(tables[0], limit=5, column_name='your_column_here')
        print(df)
    except Exception as e:
        print(f"Error retrieving data: {e}")
else:
    print("No tables found in the schema.")

