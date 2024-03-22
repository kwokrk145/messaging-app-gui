'''Module for extracting server information'''
import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
DataT = namedtuple("DataT", ["typ", "msg"])


def directmessage(json_msg, category):
    '''Extract message from server'''
    try:
        json_msg = json.loads(json_msg)
        resp = json_msg["response"]
        if resp["type"] == "error":
            return None
        typ = resp["type"]
        if category == "direct":
            message = resp["message"]
        else:
            message = resp["messages"]
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return None
    return DataT(typ, message)
