from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

AES_KEY = os.urandom(16) 

def encrypt_password(plain_text_password):
    backend = default_backend()
    
    iv = os.urandom(16)
    
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plain_text_password.encode()) + padder.finalize()

    encrypted_password = encryptor.update(padded_data) + encryptor.finalize()
    
    return iv + encrypted_password

def decrypt_password(encrypted_password_with_iv):
    backend = default_backend()

    iv = encrypted_password_with_iv[:16]
    encrypted_password = encrypted_password_with_iv[16:]
    
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()

    decrypted_padded_password = decryptor.update(encrypted_password) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    decrypted_password = unpadder.update(decrypted_padded_password) + unpadder.finalize()

    return decrypted_password.decode()

