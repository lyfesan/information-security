import sys
import os
import socket

# Import DES program
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.insert(0, parent_dir)

from DES import DES

def server_program():
    key = 'AkuKamus'
    # get the hostname
    host = socket.gethostname()
    port = 9999  # initiate port no above 1024

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = DES.batch_decrypt(str(conn.recv(1024).decode()), key)
        
        print("from connected user: " + data)
        data = input(' -> ')
        data = DES.batch_encrypt(data, key)
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()