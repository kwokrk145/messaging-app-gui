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
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
DataTuple = namedtuple('DataTuple', ['typ', 'msg', 'token'])


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
