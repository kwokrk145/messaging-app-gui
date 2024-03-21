import json
import socket
from collections import namedtuple

server = "168.235.86.101"
port = 3021
# Namedtuple to hold the values retrieved from json messages.
DataT = namedtuple("DataT", ["typ", "msg"])

def directmessage(json_msg, category):
    try:
        json_msg = json.loads(json_msg)
        resp = json_msg["response"]
        if resp["type"] == "error":
            return None
        else:
            typ = resp["type"]
            if category == "direct":
                message = resp["message"]
            else:
                message = resp["messages"]
    except json.JSONDecodeError:
            print("Json cannot be decoded.")
            return None
    return DataT(typ, message)
#x =  "this should give an error"
#print(msg_extract(x, "direct"))