import streamlit as st
import psycopg2

def get_connection():
    return psycopg2.connect(
        host=st.secrets["db"]["host"],
        user=st.secrets["db"]["user"],
        password=st.secrets["db"]["password"],
        database=st.secrets["db"]["name"],
        port=st.secrets["db"]["port"]
    )
