""" Module for AES encryption/decryption """
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad


def Encrypt(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    init_value = base64.b64encode(cipher.iv)
    ct_enc = base64.b64encode(ct_bytes)
    return ct_enc.decode('utf-8'), init_value.decode('utf-8')


def Decrypt(data, key, init_value):
    data = base64.b64decode(data)
    init_value = base64.b64decode(init_value)
    cipher = AES.new(key, AES.MODE_CBC, init_value)
    plaintext = unpad(cipher.decrypt(data), AES.block_size)
    return plaintext
