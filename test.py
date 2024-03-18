#server 168.235.86.101
#port 3021
import socket
import time
from ds_protocol import extract_json
from Profile import Profile

x = Profile()
#x.save_profile("/Users/kwokr/OneDrive/Random/dsu/dogname.dsu")
# x.username = "codewars12"
# x.password = "hi"
# x.bio = "boo"
x.load_profile("/Users/kwokr/OneDrive/Random/a5/test.dsu")
x.add_friend("tongs")
x.add_message("hi",4, "tongs", "tongs")
x.add_message("boo",2, "tongs", "tongs")
x.add_message("this shoudl be first", 1, "tongs", "myself")
x.save_profile("/Users/kwokr/OneDrive/Random/a5/test.dsu")

'''
server = "168.235.86.101"
port = 3021
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((server, port))
    print("Connected!")
except socket.gaierror:
    print("Unable to Connect. Please try again.\n")
join_msg = f'{{"join": {{"username": "{"hello32"}", "password": "{"123"}", "token": ""}}}}'
x = f'{{"token": "{"c9883ca2-e274-4916-99a8-31f5a76dc0b9"}", "directmessage": {{"entry": "Hello World!", "recipient": "statfddfadsfafadsdssrn", "timestamp": "{time.time()}"}}}}'
send = client.makefile('w')
recv = client.makefile('r')

send.write(x + '\r\n')
send.flush()

resp = recv.readline()
print(resp)



def directmessage(message, server, port, username, password):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if connect(client, server, port):
        join = f'{{"join": {{"username": "{username}", "password": "{password}", "token": ""}}}}'
        g_send = client.makefile('w')
        recv = client.makefile('r')
        g_send.write(join + '\r\n')
        g_send.flush()
        resp = recv.readline()
        data = extract_json(resp)
        token = data.token
directmessage("Fd",server,port, "hello31","123")
'''