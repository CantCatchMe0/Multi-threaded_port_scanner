import socket
import sys
from datetime import datetime
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
import threading
import argparse
from colorama import init, Fore

init(autoreset=True)

print_lock = threading.Lock()

def main():
    parser = argparse.ArgumentParser(description="Python multi-threaded_port_scanner v1.0")
    parser.add_argument("target", help = "target IP, host name or url")
    parser.add_argument("-p", "--ports", default="1-1000", help = "scan range, default 1-1000")
    parser.add_argument("-t", "--threads", type=int, default=50, help="thread number default 50")

    args = parser.parse_args()
    target_host = get_host(args.target)

    try:
        target_ip = socket.gethostbyname(target_host)
        print(f"{Fore.CYAN}[*] Target: {target_host} Resolve to IP: {target_ip}")
    except socket.gaierror:
        print(f"{Fore.RED}[!] Can not resolve the host name")
        sys.exit()  
      
    try:
        start_port, end_port = map(int, args.ports.split('-'))
        port_list = range(start_port, end_port + 1)
    except ValueError:
        print(f"{Fore.RED}[!] Port format is wrong, pleas input in start-end format example: 1-100")
        sys.exit()   
    
    print(f"{Fore.CYAN}[*] Start scanning {len(port_list)} ports, using {args.threads} of threads...")
    start_time = datetime.now()

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        for port in port_list:
            executor.submit(scan_port, target_ip, port)

    end_time = datetime.now()
    print(f"{Fore.CYAN}[*] Done total time: {end_time - start_time}")

def get_host(url):
    # urllib need url to contaim http/https, if not we will add it for resolve
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
        
    parsed_url = urlparse(url)

    return parsed_url.hostname 

def scan_port(ip, port):
    try:
        # SOCK_STREAM == TCP AF_INET == IPv4
        # I have to create a new socket every time I try to connect
        # because the state will change if it is closed or it is failed
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1) # the time out is set to be 0.5s

        # starting the connection with connect_ex
        # return 0 if it connection successed
        # return a error num if it connection failed
        result = sock.connect_ex((ip, port))
        if result == 0:
            banner = get_banner(ip, port)
            banner_str = f" Service: {banner}" if banner else ""
            with print_lock:
                print(f"{Fore.GREEN}[+] Port {port} is OPEN{Fore.RESET}{banner_str}")
        sock.close()
    except:
        pass

def get_banner(ip, port):
    # this method try to get banner from the target host
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((ip,port))

        try:
            s.send(b'HEAD / HTTP/1.0 \r\n\r\n')
        except:
            pass

        banner = s.recv(1024).decode().strip()
        s.close()
        return banner
    
    except:     
        return None

if __name__ == '__main__':
    main()
