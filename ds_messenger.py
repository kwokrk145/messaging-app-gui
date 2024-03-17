import ds_protocol
import time
import socket
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
    condition = ds_protocol.token_retrieve(self.user, self.pw, self.server, self.port)
    if condition:
        self.token = condition
        to_send = f'{{"token": "{self.token}", "directmessage": {{"entry": "{message}", "recipient": "{recipient}", "timestamp": "{time.time()}"}}}}' #change time later
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            s = client.makefile("w")
            rec = client.makefile("r")
            s.write(message + "\r\n")
            s.flush()
            info = ds_protocol.msg_extract(rec)
            if info is None:
                condition = False
            else:
               condition = True
            return condition

  def retrieve_new(self) -> list:
    # must return a list of DirectMessage objects containing all new messages
    pass
 
  def retrieve_all(self) -> list:
    # must return a list of DirectMessage objects containing all messages
    pass