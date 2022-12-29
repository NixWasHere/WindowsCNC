import base64
import socket
import time

def encode_command(command):
    return base64.b64encode(command.encode())

def send_command(conn, command):
    conn.send(encode_command(command))

def receive_output(conn):
    output = conn.recv(1024).decode()
    print(output)

def connect_to_server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock

def main():
    host = str(input("IP: "))
    port = int(input("Port: "))
    
    while True:
        try:
            
            conn = connect_to_server(host, port)
            
            while True:
                
                command = input("Enter command: ")
                
                if (command == "exit"):
                    print("Leaving...")
                    exit()
                    
                try:
                    send_command(conn, command)
                    receive_output(conn)
                    
                except ConnectionResetError:
                    print("Connection Reset, retrying...")
                    time.sleep(5)
                    conn = connect_to_server(host, port)
                    continue
                    
        except ConnectionRefusedError:
            print("Server offline, retrying in 5 seconds..")
            time.sleep(5)

if __name__ == "__main__":
    main()
