
import pg8000
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

# Get credentials from environment variables
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
database = os.getenv('DB_NAME')

try:
    # Connect to PostgreSQL using pg8000
    connection = pg8000.connect(
        user=user,
        password=password,
        host=host,
        port=int(port),
        database=database
    )

    print("Connection successful")

    # Create a cursor and fetch data
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Campaign LIMIT 10")
    rows = cursor.fetchall()
    
    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
    print(df)

except Exception as e:
    print(f"Error: {e}")
finally:
    connection.close()
    print("Connection closed")
