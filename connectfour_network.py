#This module implements the user interface for the networked version of the game
#that plays against an artificial intelligence.

import connectfour_socket
import connectfour
import collections
import socket
import connectfour_gameboard

def ask_game(connection:connectfour_socket.SocketConnection,username) -> bool:
    '''
    Sending text for asking game to the server and receive responses. If the responses are not
    we want, it return False, otherwise, it return True.
    '''
    connectfour_socket.to_write(connection,'I32CFSP_HELLO '+ username)
    response1 = connectfour_socket.read_line(connection)
    connectfour_socket.to_write(connection,'AI_GAME')
    response2 = connectfour_socket.read_line(connection)

    if response1.startswith('WELCOME') and response2 == 'READY':
        print('Game Start')
        return True

    return False


def response(connection:connectfour_socket.SocketConnection)-> str:
    '''
    Reads the response from server, a line of text sent from the server
    and returns it without a newline on the end of it
    '''
    
    responses = connectfour_socket.read_line(connection)
    return responses



def server_step(response:str,GameBoard) ->connectfour.GameState or None:
    '''
    Recording the server command and return new game board.
    The AI may send wrong command, if so the pragram will closing the connection
    and quit
    '''
    try:
        command = response.split()
        if command[0].upper() == 'DROP':
            col_num = int(command[1])
            if 1<= col_num <= connectfour.BOARD_COLUMNS: 
                NewBoard = connectfour.drop(GameBoard,col_num -1)
                return NewBoard
            else:
                pass
        elif command[0].upper() == 'POP':
            col_num = int(command[1])
            if 1<= col_num <= connectfour.BOARD_COLUMNS: 
                NewBoard = connectfour.pop(GameBoard,col_num-1)
                return NewBoard
            else:
                pass
        else:
            pass
    
    except ValueError:
            pass
    
    
def send_command(connection:connectfour_socket.SocketConnection)-> (str,int):
    '''
    Program will ask user input the command. It will ask continue until a valid
    command. Then the pragram will write the commadn to the server.
    '''
    
    command,col_num = connectfour_gameboard.check_command()
    connectfour_socket.to_write(connection,command + ' ' + str(col_num))
    return command,col_num


def client_step(command:str,col_num:int,GameBoard)-> connectfour.GameState:
    '''
    Recording the client command and return new game board
    '''
    
    if command == 'DROP':
        NewBoard = connectfour.drop(GameBoard,col_num-1)

    elif command =='POP':
        NewBoard = connectfour.pop(GameBoard,col_num-1)

    return NewBoard
    
def run_connect() ->(connectfour_socket.SocketConnection,str):
    '''
    Connects to server running on the given host and listening
    on the given port, returning a SocketConnection object describing
    that connection if successful, or raising an exception if the attempt
    to connect fails.
    If there has exception, the program will ask user to enter again.
    '''
    
    while True:
        host = connectfour_socket.the_host()
        port = connectfour_socket.the_port()
        username = connectfour_socket.the_username()
        print('Connecting to '+host + ' port: '+str(port))
        try:
            Connection = connectfour_socket.connect(host,port)
            print('Connect success')
            break
        except ConnectionRefusedError:
            print ('Refusing connect')
        except TimeoutError:
            print('Connecting time out, Connect again')
        except socket.gaierror:
            print('Invaild host, Enter again')

    return Connection, username
    
def user_inter() -> None:
    '''
    Connecting to a server and ask for game. If it's True, the program will
    start the game. It will send user's command to the server and receive
    server's command back. The all command will record and print current
    gameboard. The program will run until there is a winner come out.
    Whatever if there a exception or not, the connection will close finally
    '''

    Connection,username = run_connect()

    try:
        if ask_game(Connection,username):
            GameBoard = connectfour.new_game()
            connectfour_gameboard.print_broad(GameBoard)
            while connectfour_gameboard.check_game_over(GameBoard):
                command,col_num = send_command(Connection)

                response1 = response(Connection)
                                   
                if response1 == 'OKAY':
                    response2 = response(Connection)
                    response3 = response(Connection)
                    if response3 == 'READY' and response2 != None:
                        print('Play Yellow: '+ response2)
                        GameBoard = client_step(command,col_num,GameBoard)                
                        GameBoard = server_step(response2,GameBoard)
                        connectfour_gameboard.print_broad(GameBoard)
                    elif response3.startswith('WINNER') and response2 != None:
                        GameBoard = client_step(command,col_num,GameBoard)                
                        GameBoard = server_step(response2,GameBoard)
                        connectfour_gameboard.print_broad(GameBoard)
                    else:
                        break                    
                elif response1 == 'INVAILD':
                    response2 = response(Connection)
                    print('Invalid')
                    pass
                elif response1.startswith('WINNER'):
                    break
                else:
                    break
    finally:
        print('Closing connection now')
        connectfour_socket.close(Connection)
        print('Finishing close')


if __name__ == '__main__':
    user_inter()
