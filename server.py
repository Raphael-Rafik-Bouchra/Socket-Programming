
import os
import socket
import sys
import threading


HOST = "127.0.0.1"
PORT = 3000
server_path = 'C:/Users/michel/Desktop/Network/6171_6217_6104_Network_Project/Server Storage'
Max_File_size = 8192

def ack_request(client_socket):
    data = client_socket.recv(1024)
    print('Received {}'.format(data))
    client_socket.send('ACK!'.encode())
    return data


def check_file_in_server(file_name):
    for root, dirs, files in os.walk(server_path):
        for file in files:
            if file == file_name:
                return True
    return False

def send_file(file_name):
    flag = check_file_in_server(file_name)
    print(flag)  # to print 200 OK or 404 Not found.
    if flag:
        with open(server_path + '/' + file_name, 'rb') as handle:
            return "HTTP/1.0 200 OK" + '\r\n', handle.read()
    else:
        return "HTTP/1.0 404 Not Found" + '\r\n', None


def upload_file(file_name, data):
    with open(server_path + '/' + file_name, 'wb') as handle:
        handle.write(data)


def handle_request(conn):
    data = ack_request(conn)
    data = data.decode()

    data_options = data.split()
    command_type = data_options[0]
    file_name = data_options[1]

    if 'get' in command_type:
        status, file = send_file(file_name)
        conn.send(status.encode())
        if file:
            conn.sendall(file)
    elif 'post' in command_type:
        conn.send(("HTTP/1.0 200 OK" + '\r\n').encode())
        temp = conn.recv(Max_File_size)
        upload_file(file_name, temp)
    conn.close()

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    s.listen()

    while True:
        conn, addr = s.accept()

        print(f"Connected by {addr}")
        
        client_handler = threading.Thread(target=handle_request, args=(conn,))
        client_handler.run()
        # with conn:
        #     print(f"Connected by {addr}")
        
        #     client_handler = threading.Thread(target=handle_request, args=(conn,))
        #     client_handler.run()

        #     while True:
        #         command = conn.recv(1024)
        #         command = command.decode()
        #         print('--------HTTP Client Response--------')
        #         print(command)
        #         print('------------------------------------')
        #         break

        #     command_options = command.split()
        #     command_type = command_options[0]
        #     file_name = command_options[1]
        
        #     if 'get' in command_type:
        #         try:
        #             file_path = Server_Path + file_name
        #             f = open (file_path, "rb")
        #             data = 'HTTP/1.0 200 OK \r\n \r\n'
        #             conn.send(data.encode())
                
        #             l = f.read(1024)
        #             while (l):
        #                 conn.send(l)
        #                 l = f.read(1024) 
        #             f.close()
        #             conn.send('\r\n'.encode())

        #         except IOError:
        #             conn.send('HTTP/1.0 404 Not Found'.encode())
        #             conn.close()
      
        #     elif 'post' in command_type:
        #         lines = command.splitlines()
                
        #         data = "\n".join(lines[2:])
        #         file_path = Server_Path + file_name
        #         w = open(file_path,'w')
        #         w.write(data)
            
        #         conn.close()