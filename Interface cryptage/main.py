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
