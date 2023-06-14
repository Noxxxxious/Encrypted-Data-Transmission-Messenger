from Client import Client


if __name__ == "__main__":
    client1 = Client("localhost", 8081, 8080)
    client1.start()
