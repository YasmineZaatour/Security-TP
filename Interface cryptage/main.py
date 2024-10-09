import streamlit as st
import sqlite3

#Create a connection with users database
def db_connection ():
    conn = sqlite3.connect('users.db')
    return conn 

#Register a new user 
def register_user (username, password):
    conn = db_connection()
    c = conn.cursor()
    try:
        c.execute(''' INSERT INTO users (username, password) VALUES (?, ?) ''', (username, password))
        conn.commit()
        st.success("User registered successfully")
    except sqlite3.IntegrityError:
        st.error("Username already exists")
    finally:
        conn.close()

#Login a user
def login_user (username, password):
    conn = db_connection()
    c = conn.cursor()
    c.execute(''' SELECT * FROM users WHERE username = ? AND password = ? ''', (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

# Streamlit app
st.title("User Authentication")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Select an option", menu)

if choice == "Register":
    st.subheader("Create an Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if username and password:
            register_user(username, password)
        else:
            st.error("Please out all the fields !")

elif choice == "Login":
    st.subheader("Log In to your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login_user(username, password):
            st.success(f"Welcome back {username} !")
            #run cypher function here
        else: 
            st.error("Invalid username or password !")
            

