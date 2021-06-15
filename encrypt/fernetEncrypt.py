from cryptography.fernet import Fernet
import sys

def encrypt(key,message):
    utf_key = key.encode('utf-8')
    f = Fernet(utf_key)
    cookie_encoded = str(message).encode('utf-8')
    f.encrypt(cookie_encoded).decode('utf-8')

encrypted = encrypt(sys.argv[2],sys.argv[3])
print(encrypted)