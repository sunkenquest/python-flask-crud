import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

encryption_key = os.getenv("ENCRYPTION_KEY")


def encrypt_password(plain_text_password: str) -> str:
    """Encrypt a password using the provided encryption key."""
    f = Fernet(encryption_key)
    encrypted_password = f.encrypt(plain_text_password.encode())
    return encrypted_password.decode()


def decrypt_password(encrypted_password: str) -> str:
    """Decrypt the password using the provided encryption key."""
    f = Fernet(encryption_key)
    decrypted_password = f.decrypt(encrypted_password.encode())
    return decrypted_password.decode()
