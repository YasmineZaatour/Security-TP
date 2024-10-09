import streamlit as st
import sqlite3

#Create a connection with users database
def db_connection ():
    conn = sqlite3.connect('users.db')
    return conn 
