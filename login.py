# import streamlit as st
# import hashlib
# from db_connection import get_connection

# def login():
#     st.title("Login Form")

#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")

#     if st.button("Login"):
#         if not username or not password:
#             st.warning("Please enter both username and password.")
#             return

#         conn = get_connection()
#         cur = conn.cursor()

#         hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        
#         try:
#             # ✅ Fixed: Table name changed from 'users' → 'auth'
#             cur.execute("SELECT * FROM auth WHERE username=%s AND password=%s", (username, hashed_pw))
#             user = cur.fetchone()

#             if user:
#                 st.session_state["user"] = username
#                 st.success(f"Welcome {username}!")
#                 st.rerun()
#             else:
#                 st.error("Invalid username or password")

#         except Exception as e:
#             st.error(f"Error: {e}")
#         finally:
#             cur.close()
#             conn.close()

import streamlit as st
import hashlib
from db_connection import get_connection

def login():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #74ABE2, #5563DE);
            color: white;
        }
        .login-card {
            background-color: rgba(255, 255, 255, 0.15);
            padding: 2.5rem;
            border-radius: 20px;
            text-align: center;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 25px rgba(0,0,0,0.2);
            max-width: 400px;
            margin: auto;
        }
        input {
            border-radius: 10px !important;
        }
        .stButton>button {
            width: 100%;
            background-color: #4F8BF9;
            color: white;
            border-radius: 10px;
            height: 3rem;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # st.markdown("<div class='login-card'>", unsafe_allow_html=True)
    st.title("🔐 Login")
    st.write("Welcome back! Please login to continue.")

    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    if st.button("Login"):
        if not username or not password:
            st.warning("Please enter both username and password.")
            return

        conn = get_connection()
        cur = conn.cursor()
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()

        try:
            cur.execute("SELECT * FROM auth WHERE username=%s AND password=%s", (username, hashed_pw))
            user = cur.fetchone()
            if user:
                st.session_state["user"] = username
                st.success(f"Welcome back, {username}!")
                st.rerun()
            else:
                st.error("Invalid username or password.")
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            cur.close()
            conn.close()
    st.markdown("</div>", unsafe_allow_html=True)
