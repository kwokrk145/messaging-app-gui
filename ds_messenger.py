import ds_protocol
import time
import socket
import send_server
class DirectMessage:
  def __init__(self, r=None, msg=None, ts=None):
    self.recipient = r
    self.message = msg
    self.timestamp = ts


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.user = username
        self.pw = password
        self.server = dsuserver
        self.port = 3021
		
    def send(self, message:str, recipient:str) -> bool:
    # must return true if message successfully sent, false if send failed.
        condition = ds_protocol.token_retrieve(self.user, self.pw, \
                                               self.server, self.port)
        if condition:
            self.token = condition
            to_send = f'{{"token": "{self.token}", "directmessage":\
                        {{"entry": "{message}", "recipient": "{recipient}",\
                        "timestamp": "{time.time()}"}}}}' #change time late
            resp = send_server.response(to_send, self.server, self.port)
            info = ds_protocol.msg_extract(resp, "direct")
            if info is None:
                condition = False
            else:
                condition = True
        return condition
    
    def retrieve_new(self) -> list:
    # must return a list of DirectMessage objects containing all new messages
        messages = []
        condition = ds_protocol.token_retrieve(self.user, self.pw, \
                                               self.server, self.port)
        if condition:
            self.token = condition
            to_send = f'{{"token":"{self.token}", "directmessage": "new"}}'
            resp = send_server.response(to_send, self.server, self.port)
            info = ds_protocol.msg_extract(resp, "other").msg
            for m in info:
                m = DirectMessage(m["from"], m["message"],m["timestamp"])
                messages.append(m)
        return messages

 
    def retrieve_all(self) -> list:
    # must return a list of DirectMessage objects containing all messages
        messages = []
        condition = ds_protocol.token_retrieve(self.user, self.pw, \
                                               self.server, self.port)
        if condition:
            self.token = condition
            to_send = f'{{"token":"{self.token}", "directmessage": "all"}}'
            resp = send_server.response(to_send, self.server, self.port)
            info = ds_protocol.msg_extract(resp, "other").msg
            for m in info:
                m = DirectMessage(m["from"], m["message"], m["timestamp"])
                messages.append(m)
        return messages
  

#x = DirectMessenger("168.235.86.101", "codewars12", "hi")
#print(x.send("i hate this assignment","phonebox711"))

#l = x.retrieve_new()
#for i in l:
#    print(i.message)