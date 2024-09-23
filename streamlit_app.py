
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, exc, event, select, inspect
import streamlit as st
import os
from dotenv import load_dotenv
import psycopg2

# Load environment variables from .env file
load_dotenv()

user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
database = os.getenv('DB_NAME')
schema_name = os.getenv('schema_name')

# Create the connection string
connection_string = f'postgresql://{user}:{password}@{host}:{port}/{database}'

# Create the SQLAlchemy engine
engine = create_engine(connection_string)

# Event listener to ping the connection
@event.listens_for(engine, "engine_connect")
def ping_connection(connection, branch):
    if branch:
        # Do not ping "branched" connections (SQLAlchemy 2.x compatibility)
        return

    try:
        # Test the connection with a simple 'SELECT 1'
        connection.scalar(select(1))
    except exc.DBAPIError as err:
        # Handle invalidated connections
        if err.connection_invalidated:
            # Retry the connection
            connection.scalar(select(1))
        else:
            # Raise any other DB errors
            raise

# Streamlit app code
st.set_page_config(page_title="Remote Sensing DB", page_icon="📊")

st.title("📊 Remote Sensing Database Explorer")

st.write(
    """
    This app visualizes data from the central database maintained through a PostgreSQL server mounted on 
    [TU Dresden's secure VM](https://tu-dresden.de/zih/dienste/service-katalog/zusammenarbeiten-und-forschen/server_hosting).
    It shows the data stored in a normalized form with tables connected through Primary and Foreign keys. Just 
    click on the widgets below to explore!
    """
)

# Function to get tables in the schema
@st.cache_data
def get_tables():
    inspector = inspect(engine)
    tables = inspector.get_table_names(schema=schema_name)
    return tables

# Function to get table data
def get_table_data(table_name, limit=10, offset=0, search=''):
    with engine.connect() as connection:
        search_condition = f"WHERE column_name ILIKE '%{search}%'" if search else ''
        query = f'''
            SELECT * FROM {schema_name}.{table_name}
            {search_condition}
            LIMIT {limit} OFFSET {offset}
        '''
        data = pd.read_sql(query, connection)
    return data

# Get list of tables
tables = get_tables()

st.write(
    """
    The db is set up through snowflake schema and the main facts are stored in VehiclePassage table.
    Each Campaign is given a unique ID and all information is stored in the Campaign table.
    The ids joining the VP and Campaign are SessionIDs which are unique based on the combination of Site, Starttime, 
    Stoptime & InstrumentID. Measurement data for any particular campaign can be accessed through these SessionIDs.
    """
)

st.write(
    """ Other sub-tables include VehicleCategoryConversion,VehicleMakeCode, FuelType, EmissionStandard, Instrument 
    and Site which contains IDs acting as foreign keys for respective unique values"""
)

# Table selection
table_name = st.selectbox("Select a table", tables)

if table_name:
    st.subheader(f"Data from `{table_name}`")
    
    # Pagination and filtering inputs
    limit = st.number_input("Rows per page", min_value=1, max_value=100, value=10)
    offset = st.number_input("Offset", min_value=0, step=limit)
    search = st.text_input("Search (optional)")
    
    # Show table data
    data = get_table_data(table_name, limit, offset, search)
    st.write(data)

    # Display control options
    st.write(f"Showing rows with offset {offset}")


"""
# Show a multiselect widget with the genres using `st.multiselect`.
genres = st.multiselect(
    "Genres",
    df.genre.unique(),
    ["Action", "Adventure", "Biography", "Comedy", "Drama", "Horror"],
)

# Show a slider widget with the years using `st.slider`.
years = st.slider("Years", 1986, 2006, (2000, 2016))

# Filter the dataframe based on the widget input and reshape it.
df_filtered = df[(df["genre"].isin(genres)) & (df["year"].between(years[0], years[1]))]
df_reshaped = df_filtered.pivot_table(
    index="year", columns="genre", values="gross", aggfunc="sum", fill_value=0
)
df_reshaped = df_reshaped.sort_values(by="year", ascending=False)


# Display the data as a table using `st.dataframe`.
st.dataframe(
    df_reshaped,
    use_container_width=True,
    column_config={"year": st.column_config.TextColumn("Year")},
)

# Display the data as an Altair chart using `st.altair_chart`.
df_chart = pd.melt(
    df_reshaped.reset_index(), id_vars="year", var_name="genre", value_name="gross"
)
chart = (
    alt.Chart(df_chart)
    .mark_line()
    .encode(
        x=alt.X("year:N", title="Year"),
        y=alt.Y("gross:Q", title="Gross earnings ($)"),
        color="genre:N",
    )
    .properties(height=320)
)
st.altair_chart(chart, use_container_width=True)
"""