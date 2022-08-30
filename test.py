import socket
import json

ip = '192.168.1.11'
port = 1234

sock = socket.socket()
sock.connect((str(ip), port))
sock.send('state=?'.encode())
data = sock.recv(1024)
sock.close()
if data:
    data = data.decode()

data = json.loads(data)

if data['cmd'] == 'state':
    sn = data['sn']
    runtime = data['runtime']

for i in range(0, len(data['output'])):
    print('switch ' + str(i + 1) + ' ' + data['output'][i])

print(data['output'])


switch = 'xxxxxxxx'

num = 7

switch = ['x' for i in range(0, 8)]
switch[num - 1] = '1'

print(''.join(switch))
