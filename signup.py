# import streamlit as st
# import hashlib
# from db_connection import get_connection

# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# def signup():
#     st.title("Signup Form")

#     username = st.text_input("Username")
#     email = st.text_input("Email")
#     password = st.text_input("Password", type="password")
#     confirm_password = st.text_input("Confirm Password", type="password")

#     if st.button("Signup"):
#         if not username or not email or not password:
#             st.warning("Please fill out all fields.")
#             return
        
#         if password != confirm_password:
#             st.error("Passwords do not match!")
#             return

#         conn = get_connection()
#         cur = conn.cursor()

#         hashed_pw = hash_password(password)
#         try:
#             # ✅ Fixed: Table name changed from 'users' → 'auth'
#             cur.execute(
#                 "INSERT INTO auth (username, email, password) VALUES (%s, %s, %s)",
#                 (username, email, hashed_pw)
#             )
#             conn.commit()

#             st.success("Signup successful! Redirecting to login page...")
#             st.session_state["page"] = "Login"
#             st.rerun()

#         except Exception as e:
#             st.error(f"Error: {e}")
#         finally:
#             cur.close()
#             conn.close()


import streamlit as st
import hashlib
from db_connection import get_connection

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #FF9A8B, #FF6A88, #FF99AC);
            color: white;
        }
        .signup-card {
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
            background-color: #E94E77;
            color: white;
            border-radius: 10px;
            height: 3rem;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # st.markdown("<div class='signup-card'>", unsafe_allow_html=True)
    st.title("📝 Signup")
    st.write("Create your new account below")

    username = st.text_input("Username", placeholder="Enter a username")
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Create a password")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")

    if st.button("Sign Up"):
        if not username or not email or not password:
            st.warning("Please fill out all fields.")
            return

        if password != confirm_password:
            st.error("Passwords do not match!")
            return

        conn = get_connection()
        cur = conn.cursor()

        hashed_pw = hash_password(password)
        try:
            cur.execute(
                "INSERT INTO auth (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed_pw)
            )
            conn.commit()

            st.success("🎉 Signup successful! Redirecting to login page...")
            st.session_state["page"] = "Login"
            st.rerun()

        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            cur.close()
            conn.close()
    st.markdown("</div>", unsafe_allow_html=True)
