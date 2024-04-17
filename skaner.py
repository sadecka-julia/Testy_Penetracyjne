import socket
import ipaddress
import threading
import signal
import time

def scan_ports(target_ip, ports):
    open_ports = []

    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        result = sock.connect_ex((target_ip, port))
        if result == 0:
            open_ports.append(port)

        sock.close()

    return open_ports

def check_http_ports(open_ports):
    http_ports = [80, 443]
    for port in open_ports:
        if port in http_ports:
            return True
    return False

def scan_address(addr, min_port, max_port):
    open_ports = scan_ports(addr, range(min_port, max_port + 1))
    return addr, open_ports

def main():
    scanner_ip = "127.0.0.1"
    min_port = 1
    max_port = 1025
    threads = 10

    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sck.connect(('1.1.1.1', 1))
    ip = sck.getsockname()[0]
    sck.close()

    ip_split = ip.split('.')
    ip_base = ip_split[0] + '.' + ip_split[1] + '.' + ip_split[2] + '.'

    open_ports_list = []

    def signal_handler(signal, frame):
        print("Scan aborted.")
        for thread in threads:
            thread.join()
        exit()

    signal.signal(signal.SIGINT, signal_handler)

    for i in range(1, 255):
        if abort:
            break

        addr = ip_base + str(i)
        thread = threading.Thread(target=lambda: open_ports_list.append(scan_address(addr, min_port, max_port)))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    for host_ip, open_ports in open_ports_list:
        print(f"\nHost: {host_ip}")
        print("Open Ports:", open_ports)

        if check_http_ports(open_ports):
            print("\033[91mHTTP/HTTPS ports detected\033[0m")

if __name__ == "__main__":
    main()
