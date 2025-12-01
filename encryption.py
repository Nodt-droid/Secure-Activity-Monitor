from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import os

KEY_FILE = "aes.key"

def generate_key():
    if not os.path.exists(KEY_FILE):
        key = get_random_bytes(32)  # AES-256
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return key


def encrypt_data(data: str, key: bytes):
    data_bytes = data.encode("utf-8")

    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data_bytes)

    return base64.b64encode(cipher.nonce + tag + ciphertext).decode("utf-8")


def decrypt_data(token: str, key: bytes):
    raw = base64.b64decode(token)

    nonce = raw[:16]
    tag = raw[16:32]
    ciphertext = raw[32:]

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)

    return data.decode("utf-8")
