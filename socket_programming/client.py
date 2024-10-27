import sys
import os
import socket

# Import DES program
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.insert(0, parent_dir)

from DES import DES

def client_program():
    key = 'AkuKamus'
    host = socket.gethostname()
    port = 9999

    # Open connection to server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    message = input(" -> ") 

    while message.lower().strip() != 'exit':
        # Encrypt message
        message = DES.batch_encrypt(message, key)
        client_socket.send(message.encode())
        
        # Receive and decrypt data 
        data_raw = str(client_socket.recv(1024).decode())
        data = DES.batch_decrypt(data_raw, key)
        
        print('Raw data from server: ' + data_raw)
        print('Received from server: ' + data)

        message = input(" -> ")

    client_socket.close()

if __name__ == '__main__':
    client_program()
    