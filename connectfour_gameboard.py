#This module consists of the functions that are the same in both user interfaces.
#Prints the current game board to the console and a function that asks the
#user what move he or she would like to make next.


'''
Need some functions from connectfour.py
'''
import connectfour
from collections import namedtuple

'''
Creates a new game board. 
'''

def print_broad(GameBoard:connectfour.GameState) ->connectfour.GameState:
    '''
    Printing currently GameBoard. The broad's size is 6x7 and type 1 through 7
    on the top. Return the GameBoard value
    '''
    
    for i in range(1,connectfour.BOARD_COLUMNS+1):
        print(i,end = ' ')
    print('\n')
    for row in range(connectfour.BOARD_ROWS):
        for column in range(connectfour.BOARD_COLUMNS):
            if GameBoard.board[column][row] == connectfour.NONE:
                print('.',end = ' ')
            elif GameBoard.board[column][row] == connectfour.YELLOW:
                print('Y',end = ' ')
            elif GameBoard.board[column][row] == connectfour.RED:
                print('R',end = ' ')
        print('\n')
    return GameBoard


def drop(GameBoard:connectfour.GameState,column_num:int) ->connectfour.GameState:
    '''
    Recording the drop step and get NewBoard value. If a move
    cannot be made in the given column because the column is filled already,
    an InvalidMoveError is raised.
    '''
    
    try:
        NewBoard = connectfour.drop(GameBoard,column_num)    
        return print_broad(NewBoard)
    except connectfour.InvalidMoveError:
        print("You can't do this step\n")
        return GameBoard



def pop(GameBoard:connectfour.GameState,column_num:int) ->connectfour.GameState:
    '''
    Recording the pop step and get NewBoard value.If a move
    cannot be made in the given column because the column is filled already,
    an InvalidMoveError is raised.
    '''
    
    try:
        NewBoard = connectfour.pop(GameBoard,column_num)
        return print_broad(NewBoard)
    except connectfour.InvalidMoveError:
        print("You can't do this step\n")
        return GameBoard




def check_game_over(GameBoard:connectfour.GameState) -> bool:
    '''
    Determines the winning player in the given game state, if any.
    If there is no winner, it return False,otherwise, it return True.
    if there has winner, it will print which player win the game.
    '''
    
    if connectfour.winner(GameBoard) == connectfour.NONE:
        return True
    else:
        if connectfour.winner(GameBoard) == 1:
            turn = 'RED'
        elif connectfour.winner(GameBoard) == 2:
            turn = 'YELLOW'
        print('The winner is ' + turn)
        return False



def check_command() ->(str,int):
    '''
    Checking the command, it will ask user again if command and column number
    is valid
    Return a tuple contain the command str and column number
    '''
    
    while True:
        try:
            content = input('Enter DROP or POP + a space + column number\n')
            command = content.split()
            if command[0].upper() == 'DROP' and len(command) == 2:
                col_num = int(command[1])
                if 1<= col_num <= connectfour.BOARD_COLUMNS: 
                    return command[0].upper(),col_num
                else:
                    print('Invaild number, Enter again')
            elif command[0].upper() == 'POP' and len(command) == 2:
                col_num = int(command[1])
                if 1<= col_num <= connectfour.BOARD_COLUMNS: 
                    return command[0].upper(),col_num
                else:
                    print('Invaild number, Enter again')
            else:
                print('Invaild, Enter again')
        
        except ValueError:
                print('Invaild number, Enter again')
    
        
    
        
def run_process() ->None:
    '''
    Running the program, printing current gameboard and let user input command.
    the pragram will stop util there is a winner
    '''
    GameBoard = connectfour.new_game()
    print_broad(GameBoard)
    while check_game_over(GameBoard) == True:
        if GameBoard.turn == connectfour.RED:
            turn = 'RED'
        elif GameBoard.turn == connectfour.YELLOW:
            turn = 'YELLOW'

        print('The turn is: '+ turn + ' now')

        command,col_num = check_command()
        if command == 'DROP':
            GameBoard = drop(GameBoard,col_num-1)          
        elif command == 'POP':
            GameBoard = pop(GameBoard,col_num-1)



                
            
