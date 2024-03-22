'''Sending information to the server'''
import socket
def response(msg, server, port):
    '''Send information to server'''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((server, port))
        s = client.makefile("w")
        rec = client.makefile("r")
        s.write(msg + "\r\n")
        s.flush()
        resp = rec.readline()
        client.close()
        return resp
    
