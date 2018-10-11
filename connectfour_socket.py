#This module consists of all socket handling


import socket
from collections import namedtuple
import re

#Creating a namedtuple in order to store three things I need, the socket, input
#and output.

SocketConnection = namedtuple('SocketConnection',['socket','input','output'])


def the_host() -> str:
    '''
    Asking the user to specify what host they want to connect to,
    cntinuing to ask until a valid answer is given. An answer is
    considered vaild when user input something in.
    '''
    
    while True:
        host = input('Host: ').strip()

        if host =='':
            print('Enter again')
        else:
            return host


def the_port() -> int:
    '''
    Asking the user to specify what port they want to connect to,
    cntinuing to ask until a valid answer is given. A port must be
    an integer between 0 and 65535.
    '''
    while True:
        try:
            port = int(input('Post: ').strip())

            if port< 0 or port > 65535:
                print('Invalid number, enter again')
            else:
                return port
        except ValueError:
            print('Not a number,enter again')

def the_username() ->str:
    '''
    Asking the user to specify what host they want to connect to,
    cntinuing to ask until a valid answer is given. An username
    cannot contain any whitespace characters.
    '''
    while True:
        username = input('username: ')
        m = re.search('\s',username)
        if m:
            print('Invalid username,enter again')
        else:
            return username
        

def to_write(connection:SocketConnection ,content:str) ->None:
    '''
    Writes a line of text to the server, including the appropriate
    newline sequence, and ensures that it is sent immediately.
    '''
    connection.output.write(content + '\r\n')
    connection.output.flush()

    
def read_line(connection:SocketConnection) ->str:
    '''
    Reads a line of text sent from the server and returns it without
    a newline on the end of it
    '''
    
    line = connection.input.readline()[:-1]
    return line

def connect(host:str,port:int) -> SocketConnection:
    '''
    Connects to a server running on the given host and listening
    on the given port, returning a SocketConnection object describing
    that connection if successful.
    '''

    sock = socket.socket()
    sock.connect((host, port))
    sock_input = sock.makefile('r')
    sock_output = sock.makefile('w')

    return SocketConnection(socket = sock, input = sock_input,
                            output = sock_output)
    


def close(connection:SocketConnection) -> None:
    '''Closes the connection to the server'''
    connection.input.close()
    connection.output.close()
    connection.socket.close()


