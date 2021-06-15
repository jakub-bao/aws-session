from cryptography.fernet import Fernet
import sys

def encrypt(key,message):
    utf_key = key.encode('utf-8')
    f = Fernet(utf_key)
    cookie_encoded = str(message).encode('utf-8')
    return f.encrypt(cookie_encoded).decode('utf-8')

key = sys.argv[1]
msg = sys.argv[2]
encrypted = encrypt(key,msg)
print(encrypted)