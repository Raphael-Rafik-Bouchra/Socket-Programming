
import socket
import sys
import os


command_file = open(r'C:/Users/michel/Desktop/Network/6171_6217_6104_Network_Project/Client Strorage/commands.txt','r')
client_path = 'C:/Users/michel/Desktop/Network/6171_6217_6104_Network_Project/Client Strorage'
Max_File_size = 8192


def is_file(file_name_):  # Check if file is in client folder or not.
    dir_path = client_path
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file == file_name_:
                return True
    return False


def send_file(file_name):  # Check for a file and return its content.
    flag = is_file(file_name)
    if flag:
        with open(client_path + '/' + file_name, 'rb') as handle:
            return handle.read()


def write_file(file_name, data):  # Write a file to client folder.
    with open(client_path + '/' + file_name, 'wb') as handle:
        handle.write(data)




for command in command_file.readlines():
    command_options = command.split()
    command_type = command_options[0]
    # print(command_type)
    file_name = command_options[1]
    host_name = command_options[2]
    if command_options[3]:
        port_number:int = int(command_options[3])
    else:
        port_number = 80    
        
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as connection:
        # Connection established
        try:
            connection.connect((host_name, port_number))
        except:
            print('Could not connect to server')
            sys.exit(0)
        
        # Reciving permission from server
        # Sending command
       # byte_command = input(command)
        connection.sendall(command.encode())
        ack = connection.recv(1024)

        if ack:
            response = connection.recv(1024).decode()  # Receive status (200 OK or 404 Not found)
            print('--------HTTP Server Response--------')
            print(response)
            print('------------------------------------')

            if response.startswith("HTTP/1.0 200 OK"):
                if 'get' in command_type:
                    data = connection.recv(Max_File_size)
                    write_file(file_name, data)
                elif 'post' in command_type:
                    connection.sendall(send_file(file_name))
            elif response.startswith("HTTP/1.1 200 OK"):
                header_file = response.split("\r\n")
                header_file_lines = header_file[0].splitlines()

                user_agent = header_file_lines[1]
                accept = header_file_lines[2]
                accept_language = header_file_lines[3]
                accept_encoding = header_file_lines[4]
                header_connection = header_file_lines[5]
                upgrade_insecure_requests = header_file_lines[6]
                content_type = header_file_lines[7]
                content_length = header_file_lines[8]

                if 'get' in command_type:
                    data = connection.recv(int(content_length))
                    write_file(file_name, data)
                elif 'post' in command_type:
                    connection.sendall(send_file(file_name))

#-----------------------------------------------------------------------------

#         if 'get' in command_type:
#             # recieve data from server indicating the buffer size
#             #TODO: receive server response 
#             #1- 200 ok --> receive data
#             #2- 404 Not Found --> close connection
#             print('--------HTTP Server Response--------')
#             response = connection.recv(1024)
#             response = response.decode()
#             print(response)
#             print('------------------------------------')
#             if '200' in response:
#                 #TODO parse the response
#                 lines = response.splitlines()
                
#                 line_tokens = lines[0].split()
#                 HTTP_version = line_tokens[0]
#                 message_code = line_tokens[1]
#                 message_label = line_tokens[2]
                
#                 data = "\n".join(lines[2:])
#                 file_path = client_path + file_name
#                 w = open(file_path,'w')
#                 w.write(data)
            
#             connection.close()
            
#         elif 'post' in command_type:
#             f = open (client_path + file_name, "rb")
#             l = f.read(1024)
#             connection.send('\r\n \r\n'.encode())
#             while (l):
#                 connection.send(l)
#                 l = f.read(1024) 
#             connection.send('\r\n'.encode())
#             f.close()
#             connection.close()  
#         print('Connection Closed')       
# # loop on requests