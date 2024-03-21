import server_commands
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
        try:
            condition = server_commands.token_retrieve(self.user, self.pw, \
                                                self.server, self.port)
            if condition:
                self.token = condition
                to_send = f'{{"token": "{self.token}", "directmessage":\
                            {{"entry": "{message}", "recipient": "{recipient}",\
                            "timestamp": "{time.time()}"}}}}' #change time late
                resp = send_server.response(to_send, self.server, self.port)
                info = ds_protocol.directmessage(resp, "direct")
                if info is None:
                    condition = False
                else:
                    condition = True
        except (TypeError, OSError):
            condition = False
        return condition
    
    def retrieve_new(self) -> list:
    # must return a list of DirectMessage objects containing all new messages
        try:
            messages = []
            condition = server_commands.token_retrieve(self.user, self.pw, \
                                                self.server, self.port)
            if condition:
                self.token = condition
                to_send = f'{{"token":"{self.token}", "directmessage": "new"}}'
                resp = send_server.response(to_send, self.server, self.port)
                info = ds_protocol.directmessage(resp, "other").msg
                for m in info:
                    m = DirectMessage(m["from"], m["message"],m["timestamp"])
                    messages.append(m)
                return messages
            else:
                return None
        except (TypeError, OSError):
            return None

 
    def retrieve_all(self) -> list:
    # must return a list of DirectMessage objects containing all messages
        try:
            messages = []
            condition = server_commands.token_retrieve(self.user, self.pw, \
                                                self.server, self.port)
            if condition:
                self.token = condition
                to_send = f'{{"token":"{self.token}", "directmessage": "all"}}'
                resp = send_server.response(to_send, self.server, self.port)
                info = ds_protocol.directmessage(resp, "other").msg
                for m in info:
                    m = DirectMessage(m["from"], m["message"], m["timestamp"])
                    messages.append(m)
                return messages
            else:
                return None
        except (TypeError, OSError):
            return None
