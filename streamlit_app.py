
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, select, text, func

# Create the connection string
connection_string = f'postgresql://{user}:{password}@{host}:{port}/{database}'

# Create the engine
engine = create_engine(connection_string)

# Define connection parameters
user = 'lkp'
password = 'voeko'
host = '172.26.63.252'
port = '5432'
database = 'postgres'
schema_name = 'rsdb'

# Show the page title and description.
st.set_page_config(page_title="Remote Sensing DB", page_icon="📊")
st.title("📊 rsdb")
st.write(
    """
    This app visualizes data from the central database maintained through PostgreSQL server mounted on [TU Dresden's secure VM](https://tu-dresden.de/zih/dienste/service-katalog/zusammenarbeiten-und-forschen/server_hosting).
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

# Streamlit app
st.title("PostgreSQL Schema Explorer")

# Get list of tables
tables = get_tables()

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

# Load the data from a CSV. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets).
@st.cache_data
def load_data():
    df = pd.read_csv("data/movies_genres_summary.csv")
    return df


df = load_data()

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
