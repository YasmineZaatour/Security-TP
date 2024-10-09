import streamlit as st
import sqlite3
import smtplib
import random
import re
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
def login_user(email, password):
    conn = db_connection()
    c = conn.cursor()
    c.execute(''' SELECT * FROM users WHERE email = ? AND password = ? ''', (email, password))
    user = c.fetchone()
    conn.close()
    return user

# Function to send verification code
def send_verification_code(email):
    code = random.randint(100000, 999999)  # Generate a random 6-digit code
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login("your_email@gmail.com", "your_app_password")  # Replace with your email credentials
            message = f"Subject: Verification Code\n\nYour verification code is: {code}"
            server.sendmail("your_email@gmail.com", email, message)  # Send the email
        return code  # Return the generated verification code
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")  # Display error in Streamlit
        return None  # Return None if the email sending fails

# Initialize session state for logged in status and page choice
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'choice' not in st.session_state:
    st.session_state.choice = "Login"
if 'verification_code' not in st.session_state:
    st.session_state.verification_code = None
if 'email' not in st.session_state:
    st.session_state.email = None

# Validation Patterns
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
USERNAME_PATTERN = r'^[a-zA-Z0-9]{3,15}$'  # Alphanumeric, 3-15 characters
PASSWORD_PATTERN = r'^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$'  # At least 8 characters, one uppercase, one digit

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
    
    if st.button("Register"):
        if email and username and password:
            if validate_input(email, username, password):
                register_user(email, username, password)
        else:
            st.error("Please fill out all fields!")

elif choice == "Login":
    if st.session_state.logged_in:
        st.success(f"Welcome back !")
        cypher_app()  # Show the cryptography app
    else:
        st.subheader("Log In to your Account")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            user = login_user(email, password)
            if user:
                st.session_state.email = user[0]  # Assuming email is the first column
                st.session_state.verification_code = send_verification_code(st.session_state.email)  # Send verification code
                if st.session_state.verification_code:
                    st.success("Verification code sent to your email. Please check your inbox.")
                else:
                    st.error("Failed to send verification code.")
            else:
                st.error("Invalid email or password!")
        
        # MFA verification
        if st.session_state.verification_code is not None:
            mfa_code = st.text_input("Enter the verification code sent to your email")
            if st.button("Verify Code"):
                if mfa_code and int(mfa_code) == st.session_state.verification_code:
                    st.success("MFA verification successful!")
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    cypher_app()  # Show the cryptography app after successful verification
                else:
                    st.error("Invalid verification code!")
