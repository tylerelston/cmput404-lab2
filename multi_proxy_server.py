#!/usr/bin/env python3
import socket
import time, sys
from multiprocessing import Process

#define address & buffer size
# connect to proxy start
HOST = "localhost"
PORT = 8001
BUFFER_SIZE = 1024



def main():
    extern_host = 'www.google.com'
    extern_port = 80
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print('Starting proxy server')
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #bind socket to address
        proxy_start.bind((HOST, PORT))
        #set to listening mode
        proxy_start.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = proxy_start.accept()
            print("Connected by", addr)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print('Connecting to Google')
                remote_ip = get_remote_ip(extern_host) 
                proxy_end.connect((remote_ip, extern_port))

                p = Process(target=handle_request, args=(addr, conn))
                p.daemon = True
                p.start()
                print('Started process', p)

            conn.close()

def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def handle_request(addr, conn):
    print("Connected by", addr)
    full_data = conn.recv(BUFFER_SIZE)
    conn.sendall(full_data)
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()          

if __name__ == "__main__":
    main()
