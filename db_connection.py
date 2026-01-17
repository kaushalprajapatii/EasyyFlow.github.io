import streamlit as st
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host=st.secrets["db"]["host"],
        user=st.secrets["db"]["user"],
        password=st.secrets["db"]["password"],
        database=st.secrets["db"]["name"],
        port=st.secrets["db"]["port"]
    )
