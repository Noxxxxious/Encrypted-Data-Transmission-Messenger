from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64


def generate_key_pair():
    key = RSA.generate(2048)
    public_key = key.publickey().export_key().decode()
    private_key = key.export_key().decode()

    with open("private_key.pem", "w") as f:
        f.write(private_key)

    return public_key, private_key


def rsa_encode(text, public_key):
    key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(key)
    encoded_text = cipher.encrypt(text.encode())

    return base64.b64encode(encoded_text).decode()


def rsa_decode(encoded_text, private_key):
    key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(key)
    decoded_text = cipher.decrypt(base64.b64decode(encoded_text.encode()))

    return decoded_text.decode()
