import sqlite3
import pandas as pd

DB_NAME = "esg.db"

def save_to_db(df):
    conn = sqlite3.connect(DB_NAME)
    df.to_sql("esg_data", conn, if_exists="replace", index=False)
    conn.close()

def get_top_companies(limit=5):
    conn = sqlite3.connect(DB_NAME)
    query = f"""
        SELECT company, ESG_score, Risk_Level
        FROM esg_data
        ORDER BY ESG_score DESC
        LIMIT {limit}
    """
    result = pd.read_sql(query, conn)
    conn.close()
    return result

def get_average_score():
    conn = sqlite3.connect(DB_NAME)
    query = "SELECT AVG(ESG_score) as avg_score FROM esg_data"
    result = pd.read_sql(query, conn)
    conn.close()
    return round(result['avg_score'][0], 2)