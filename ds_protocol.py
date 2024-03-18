# ds_protocol.py

# Starter code for assignment 3 in ICS 32
# Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Ryan Kwok
# kwokrk@uci.edu
# 34207460

'''
Format responses from server and formats messages to send
to server
'''

import json
import socket
from collections import namedtuple

server = "168.235.86.101"
port = 3021
# Namedtuple to hold the values retrieved from json messages.
DataTuple = namedtuple('DataTuple', ['typ', 'msg', 'token'])
DataT = namedtuple("DataT", ["typ", "msg"])

def extract_json(json_msg: str) -> DataTuple:
    '''
    Call the json.loads function on a json string
    and convert it to a DataTuple object
    '''
    try:
        json_obj = json.loads(json_msg)
        resp = json_obj["response"]
        typ = resp["type"]
        msg = resp["message"]
        if typ == "error":
            token = None
        else:
            token = resp["token"]
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
    return DataTuple(typ, msg, token)


def dsp_formatting(token, typ, entry, time):
    '''
    Format user extracted information to follow
    DSP protocol
    '''
    final = f'{{"token": "{token}", "{typ}":\
        {{"entry": "{entry}", "timestamp": "{time}"}}}}'
    return final


def msg_extract(json_msg, category):
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


def connect(client, server, port, needed=None):
    if needed:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server, port))
        return True
    except socket.gaierror:
        print("Unable to connect. Please try again.")
    except socket.error:
        print("Something went wrong. Please try again.")
    return False


def token_retrieve(user, pw, server, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if connect(client, server, port):
        join_msg = f'{{"join": {{"username": "{user}", "password": "{pw}", "token": ""}}}}'
        g_send = client.makefile('w')
        recv = client.makefile('r')
        g_send.write(join_msg + '\r\n')
        g_send.flush()
        resp = recv.readline()
        data = extract_json(resp)
        client.close()
        return data.token
    client.close()
    return False