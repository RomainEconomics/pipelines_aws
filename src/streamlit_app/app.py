import streamlit as st
import pandas as pd
import psycopg2
import os

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

user=os.getenv("RDS_POSTGRES_USERNAME", "")
password=os.getenv("RDS_POSTGRES_PASSWORD", "")
host=os.getenv("RDS_POSTGRES_HOST", "")
port=int(os.getenv("RDS_POSTGRES_PORT", 5432))

connection = psycopg2.connect(user=user,
                              password=password,
                              host=host,
                              port=port)
cursor = connection.cursor()
cursor.execute("""SELECT * FROM twitter_trends""")
df = pd.DataFrame(cursor.fetchall(), columns=["date", "name", "url", "query", "tweet_volume"])

st.title('Uber pickups in NYC')
st.dataframe(df)