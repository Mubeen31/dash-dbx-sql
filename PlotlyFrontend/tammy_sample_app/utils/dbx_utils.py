from databricks import sql
from dotenv import load_dotenv
import os
import numpy as np
import pandas as pd

load_dotenv()

SERVER_HOSTNAME = os.getenv("SERVER_HOSTNAME")
HTTP_PATH = os.getenv("HTTP_PATH")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

DB_NAME = "plotly_iot_dashboard"
USER_TABLE = "silver_users"
DEVICE_TABLE = "silver_sensors"


def get_user_data(xaxis, comp):
    """
    Fetches data from the Databricks database and returns it as a pandas dataframe

    Returns
    -------
    df : pandas dataframe
        basic query of data from Databricks as a pandas dataframe
    """
    with sql.connect(
        server_hostname=SERVER_HOSTNAME,
        http_path=HTTP_PATH,
        access_token=ACCESS_TOKEN,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT {xaxis}, {comp}, risk, Count(*) AS Total 
                FROM(
                    SELECT
                    CASE WHEN gender='F' THEN 'Female' ELSE 'Male' END AS sex,
                    age, height, weight, 
                    CASE WHEN smoker='N' THEN 'Non-smoker' ELSE 'Smoker' END AS Smoker,
                    cholestlevs AS cholesterol, bp AS bloodpressure, risk
                    FROM {DB_NAME}.{USER_TABLE}
                )
                GROUP BY {xaxis}, {comp}, risk
                """
            )
            df = cursor.fetchall_arrow()
            df = df.to_pandas()
    return df
