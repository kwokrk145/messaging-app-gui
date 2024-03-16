#server 168.235.86.101
#port 3021
import socket
import time
server = "168.235.86.101"
port = 3021
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((server, port))
    print("Connected!")
except socket.gaierror:
    print("Unable to Connect. Please try again.\n")
join_msg = f'{{"join": {{"username": "{"hello32"}", "password": "{"123"}", "token": ""}}}}'
x = f'{{"token": "{"c9883ca2-e274-4916-99a8-31f5a76dc0b9"}", "directmessage": {{"entry": "Hello World!", "recipient": "statsrn", "timestamp": "{time.time()}"}}}}'
send = client.makefile('w')
recv = client.makefile('r')

send.write(x + '\r\n')
send.flush()

resp = recv.readline()
print(resp)

def connect(client, server, port):
    try:
        client.connect((server, port))
        return True
    except socket.gaierror:
        print("Unable to connect. Please try again.")
    except socket.error:
        print("Something went wrong. Please try again.")
    return False
    