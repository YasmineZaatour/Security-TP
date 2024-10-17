import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def generate_aes_key():
    """Generate a random AES-256 key."""
    return os.urandom(32)  

def encrypt_password(plain_text_password, key):
    """Encrypt a password using AES-256."""
    backend = default_backend()
    iv = os.urandom(16) 
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plain_text_password.encode()) + padder.finalize()

    encrypted_password = encryptor.update(padded_data) + encryptor.finalize()
    
    return (iv + encrypted_password).hex()  

def decrypt_password(encrypted_password_with_iv_hex, key):
    """Decrypt a password using AES-256."""
    backend = default_backend()
    encrypted_password_with_iv = bytes.fromhex(encrypted_password_with_iv_hex)  
    iv = encrypted_password_with_iv[:16]  
    encrypted_password = encrypted_password_with_iv[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()

    decrypted_padded_password = decryptor.update(encrypted_password) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_password = unpadder.update(decrypted_padded_password) + unpadder.finalize()

    return decrypted_password.decode()
