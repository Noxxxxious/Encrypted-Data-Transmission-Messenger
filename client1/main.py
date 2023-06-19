from Crypto.Random import get_random_bytes

from Client import Client
from rsa_funcs import *
from ecb_funcs import *
from cbc_funcs import *

if __name__ == "__main__":
    client1 = Client("localhost", 8080, 8081)
    client1.start()
