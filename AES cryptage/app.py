import streamlit as st
from cryptage_AES import encrypt_password, decrypt_password

st.title("AES Encryption and Decryption")

# Input for encryption
message = st.text_input("Enter the message to encrypt")

if st.button("Encrypt"):
    if message:
        encrypted_message = encrypt_password(message)
        st.write("Encrypted message (in bytes):")
        st.code(encrypted_message)
    else:
        st.error("Please enter a message to encrypt!")

# Input for decryption
encrypted_message_input = st.text_input("Enter the encrypted message 128 bits to decrypt")

if st.button("Decrypt"):
    if encrypted_message_input:
        try:
            # Convert input string to bytes
            encrypted_message_bytes = eval(encrypted_message_input)
            decrypted_message = decrypt_password(encrypted_message_bytes)
            st.write("Decrypted message:")
            st.code(decrypted_message)
        except Exception as e:
            st.error(f"Failed to decrypt the message: {e}")
    else:
        st.error("Please enter the encrypted message in bytes!")
