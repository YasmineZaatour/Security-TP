# Import necessary libraries
import streamlit as st
import sqlite3
import random
import re
from app import cypher_app

# Create a connection with users database
def db_connection():
    conn = sqlite3.connect('users.db')
    return conn 

# Register a new user 
def register_user(email, username, password, role='user'):
    conn = db_connection()
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO users (email, username, password, role) 
            VALUES (?, ?, ?, ?)
        ''', (email, username, password, role))
        conn.commit()
        st.success("User registered successfully!")
    except sqlite3.IntegrityError:
        st.error("Email or username already exists!")
    finally:
        conn.close()

# Login a user
def login_user(email, password):
    conn = db_connection()
    c = conn.cursor()
    c.execute(''' SELECT * FROM users WHERE email = ? AND password = ? ''', (email, password))
    user = c.fetchone()
    conn.close()
    return user

# Function to send verification code to terminal
def send_verification_code():
    code = random.randint(100000, 999999)  
    print(f"Your verification code is: {code}")  
    return code  

# Initialize session state for logged in status and page choice
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'choice' not in st.session_state:
    st.session_state.choice = "Login"
if 'verification_code' not in st.session_state:
    st.session_state.verification_code = None
if 'email' not in st.session_state:
    st.session_state.email = None
if 'username' not in st.session_state:  
    st.session_state.username = None

# Validation Patterns
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
USERNAME_PATTERN = r'^[a-zA-Z0-9]{3,15}$'  
PASSWORD_PATTERN = r'^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$'  

# Function to validate user input
def validate_input(email, username, password):
    if not re.match(EMAIL_PATTERN, email):
        st.error("Invalid email format!")
        return False
    if not re.match(USERNAME_PATTERN, username):
        st.error("Username must be 3-15 alphanumeric characters!")
        return False
    if not re.match(PASSWORD_PATTERN, password):
        st.error("Password must be at least 8 characters long, include at least one uppercase letter and one digit!")
        return False
    return True

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
    role = st.selectbox("Select Role", ["user", "admin"])

    if st.button("Register"):
        if email and username and password:
            if validate_input(email, username, password):
                register_user(email, username, password,role)
                st.session_state.username = username  
        else:
            st.error("Please fill out all fields!")
elif choice == "Login":
    if st.session_state.logged_in:
        st.success(f"Welcome back, {st.session_state.username}!")  
        cypher_app()  
    else:
        st.subheader("Log In to your Account")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            user = login_user(email, password)
            if user:
                st.session_state.email = user[0]  
                st.session_state.username = user[1] 
                st.session_state.role = user[3] 
                st.session_state.verification_code = send_verification_code()  
                st.success("Verification code printed to terminal. Please check your terminal.")
            else:
                st.error("Invalid email or password!")
        
        # MFA verification
        if st.session_state.verification_code is not None:
            mfa_code = st.text_input("Enter the verification code sent to your terminal")
            if st.button("Verify Code"):
                if mfa_code and int(mfa_code) == st.session_state.verification_code:
                    st.success("MFA verification successful!")
                    st.session_state.logged_in = True
                    cypher_app() 
                else:
                    st.error("Invalid verification code!")
