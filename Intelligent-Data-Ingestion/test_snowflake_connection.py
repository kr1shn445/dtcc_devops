
import os
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

try:
    connection = snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE")
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            CURRENT_USER(),
            CURRENT_ROLE(),
            CURRENT_WAREHOUSE(),
            CURRENT_DATABASE()
    """)

    print("Snowflake connection successful!")
    print(cursor.fetchone())

    cursor.close()
    connection.close()

except Exception as error:
    print("Snowflake connection failed:")
    print(error)
