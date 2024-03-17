import ds_protocol
import socket
import time
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "168.235.86.101"
port = 3021
client.connect((server, port))
x = f'{{"token": "{"c9883ca2-e274-4916-99a8-31f5a76dc0b9"}", "directmessage": {{"entry": "hola", "recipient": "codewars12", "timestamp": "{time.time()}"}}}}'
user = f'{{"token":"{"a6739a3f-c848-4b50-aeed-9c028cdaa994"}", "directmessage": "all"}}'
send = client.makefile('w')
recv = client.makefile('r')

send.write(x + '\r\n')
send.flush()


resp = recv.readline()

print(ds_protocol.msg_extract(resp, "direct"))
