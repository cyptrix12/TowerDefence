from network import NetworkManager

if __name__ == "__main__":
    NM = NetworkManager("192.168.100.9", 9999)
    NM.send_message({"action": "test", "data": "Hello, World!"})
    while True:
        continue