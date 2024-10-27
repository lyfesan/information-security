import sys
import os
import socket

# Import DES program
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.insert(0, parent_dir)

from DES import DES

def server_program():
    key = 'AkuKamus' # key used for DES
    host = socket.gethostname()
    port = 9999 

    # Create socket connection
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))

    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream and decrypt it
        data_raw = str(conn.recv(1024).decode())
        data = DES.batch_decrypt(data_raw, key)
        
        print("Raw data from connected user: " + data_raw)
        print("from connected user: " + data)
        
        # Send data to client
        data = input(' -> ')
        # Encrypt data
        data = DES.batch_encrypt(data, key)
        conn.send(data.encode())

    conn.close()

if __name__ == '__main__':
    server_program()