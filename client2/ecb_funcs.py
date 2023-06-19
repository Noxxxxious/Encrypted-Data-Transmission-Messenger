import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def ecb_encrypt(text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_text = pad(text.encode(), AES.block_size)
    cipher_text = cipher.encrypt(padded_text)

    return cipher_text


def ecb_decrypt(cipher_text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decoded_cipher_text = base64.b64decode(cipher_text)
    decrypted_text = cipher.decrypt(decoded_cipher_text)
    plain_text = unpad(decrypted_text, AES.block_size)

    return plain_text.decode()
