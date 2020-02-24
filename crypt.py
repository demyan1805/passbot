from Crypto.Cipher import AES
import hashlib
from config import secret

def getHash(data):
    hash = hashlib.sha256(bytes(data, 'utf-8')).hexdigest()
    return hash

def encode(userID, data):
    key = bytes(userID + secret, 'utf-8')
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    cipherText = cipher.encrypt_and_digest(bytes(data, 'utf-8'))[0]
    return [cipherText.hex(), nonce.hex()]

def decode(userID, data, nonce):
    key = bytes(userID + secret, 'utf-8')
    cipher = AES.new(key, AES.MODE_EAX, nonce=bytes.fromhex(nonce))
    text = cipher.decrypt(bytes.fromhex(data))
    return str(text, 'utf-8')
