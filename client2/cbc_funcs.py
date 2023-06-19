from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


def cbc_encrypt(text, key):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_text = pad(text.encode(), AES.block_size)
    cipher_text = cipher.encrypt(padded_text)

    return iv + cipher_text


def cbc_decrypt(cipher_text, key):
    iv = cipher_text[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_text = cipher.decrypt(cipher_text[AES.block_size:])
    plain_text = unpad(decrypted_text, AES.block_size)

    return plain_text.decode()
