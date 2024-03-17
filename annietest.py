import socket
import json
from collections import namedtuple
import time
DataTuple = namedtuple('DataTuple', ['response_type', 'token'])


def extract_json(json_msg: str) -> DataTuple:
    """
    Call the json.loads function on a json string and convert it to a DataTuple object.
    """
    try:
        json_obj = json.loads(json_msg)
        token = None
        response_type = json_obj['response']['type']
        if response_type == "ok":
            token = json_obj['response']['token']

    except json.JSONDecodeError:
        print("Json cannot be decoded.")

    return DataTuple(response_type, token)
def gettoken(user: str, pw: str, server: str, port: int):
    joining = f'{{"join": {{"username": "{user}", "password": "{pw}", "token": ""}}}}'

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serve:

        serve.connect((server, port))

        sending = serve.makefile("w")
        recieve = serve.makefile('r')

        sending.write(joining + '\r\n')
        sending.flush()
        serve.send(joining.encode('utf-8'))

        msg_back = recieve.readline()

        response = extract_json(msg_back)
        token = response[1]

        serve.close()
        return token


crack = gettoken("phonebox172", "123", "168.235.86.101", 3021)
tok = gettoken('circlesquare11', '123', "168.235.86.101", 3021)


def directmessage(token:str, server: str, port: int, recipient="all", message=None):
    """recipient argument takes a recipient or all or new."""
    if message:
        will_send = f'{{"token": "{token}", "directmessage": {{"entry": "{message}", "recipient": "{recipient}", "timestamp": "{time.time()}"}}}}'
    elif recipient == "new":
        will_send = f'{{"token": "{token}", "directmessage": "new"}}'
    elif recipient == "all":
        will_send = f'{{"token": "{token}", "directmessage": "all"}}'

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serve:

        serve.connect((server, port))

        sending = serve.makefile('w')
        recieve = serve.makefile('r')

        sending.write(will_send + '\r\n')
        sending.flush()
        #serve.send(will_send.encode('utf-8'))

        msg_back = recieve.readline()
        print(msg_back)

        serve.close()

        

    # if message:
    #     return msg_back["response"]["messages"]
    # else:
    #     return msg_back["response"]["messages"][0]


directmessage(crack, "168.235.86.101", 3021, "codewars132", "once")