import secrets

from Client import Client
from rsa_funcs import *
from cbc_funcs import *
from ecb_funcs import *

if __name__ == "__main__":
    client2 = Client("localhost", 8081, 8080)
    client2.start()
