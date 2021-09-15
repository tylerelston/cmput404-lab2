#!/usr/bin/env python3
import socket
import time, sys

#define address & buffer size
# connect to proxy start
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def main():
    # connect to proxy end
    extern_host = 'www.google.com'
    extern_port = 80
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
    
        print('Starting proxy server')
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        proxy_start.bind((HOST, PORT))
        #set to listening mode
        proxy_start.listen(1)
        
        #continuously listen for connections
        while True:
            conn, addr = proxy_start.accept()
            print("Connected by", addr)
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("Connecting to Google")
                remote_ip = get_remote_ip(extern_host)

                # connect proxy end
                proxy_end.connect((remote_ip, extern_port))

                send_full_data = conn.recv(BUFFER_SIZE)
                print("Sending data to google", send_full_data)
                proxy_end.sendall(send_full_data)

                proxy_end.shutdown(socket.SHUT_WR)

                data = proxy_end.recv(BUFFER_SIZE)
                print("Sending recieved data to client",data)
                conn.send(data)

                conn.close()

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip            

if __name__ == "__main__":
    main()
