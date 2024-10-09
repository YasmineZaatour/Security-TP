import streamlit as st
import sqlite3
from app import cypher_app

# Create a connection with users database
def db_connection():
    conn = sqlite3.connect('users.db')
    return conn 

# Register a new user 
def register_user(email, username, password):
    conn = db_connection()
    c = conn.cursor()
    try:
        c.execute(''' INSERT INTO users (email, username, password) VALUES (?, ?, ?) ''', (email, username, password))
        conn.commit()
        st.success("User registered successfully!")
        st.session_state.choice = 'Login'
    except sqlite3.IntegrityError:
        st.error("Email or username already exists!")
    finally:
        conn.close()

# Login a user
def login_user(username, password):
    conn = db_connection()
    c = conn.cursor()
    c.execute(''' SELECT * FROM users WHERE username = ? AND password = ? ''', (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

# Initialize session state for logged in status and page choice
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'choice' not in st.session_state:
    st.session_state.choice = "Login"

# Only show the title if the user is not logged in
if not st.session_state.logged_in:
    st.title("User Authentication")

# Sidebar menu
menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Select an option", menu, index=menu.index(st.session_state.choice))

if choice == "Register" and not st.session_state.logged_in:
    st.subheader("Create an Account")
    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if email and username and password:
            register_user(email, username, password)
            # No need for experimental_rerun
        else:
            st.error("Please fill out all fields!")

elif choice == "Login":
    if st.session_state.logged_in:
        st.success(f"Welcome back {st.session_state.username}!")
        cypher_app()  # Show the cryptography app
    else:
        st.subheader("Log In to your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome back, {username}!")
            else:
                st.error("Invalid username or password!")
