from Client import Client


if __name__ == "__main__":
    client1 = Client("localhost", 8080, 8081)
    client1.start()
