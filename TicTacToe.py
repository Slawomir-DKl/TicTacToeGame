def display_board(board):  # Printing the current board

    # Board layout elements
    horiz = "+-----+-----+-----+"
    lft = "| "
    btwn = " | "
    rght = " |"

    # Printing the board
    print(horiz, sep='\n')
    print(lft, board[0][0], btwn, board[0][1], btwn, board[0][2], rght)
    print(horiz, sep='\n')
    print(lft, board[1][0], btwn, board[1][1], btwn, board[1][2], rght)
    print(horiz, sep='\n')
    print(lft, board[2][0], btwn, board[2][1], btwn, board[2][2], rght)
    print(horiz, sep='\n')


def enter_move(board):  # User's move & board update

    # Asking user for input and checking it
    while True:
        try:
            move = int(input("Please enter number of square to put your mark: "))
            # Checking if number is > 0
            if move <= 0:
                chk = move / (move - move) # Generating ZeroDivisionError
            # Calculating row and column @
            if move % 3 == 0:
                r = (move - move % 3) // 3 - 1
                c = 2
            else:
                r = (move - move % 3) // 3
                c = move % 3 - 1
            if board[r][c] == move:  # Checking if the square is empty
                # Updating square
                board[r][c] = "O"
                break
            else:
                chk = nofunct #non-existing function to generate the ValueError
        except ValueError:
            print("It is not an integer!")
        except NameError:
            print("This square is occupied")
        except:
            print("The number is not in the range from 1 to 9")


def make_list_of_free_fields(board):  # Building list of all the free squares

    free = []
    for x in range(3):
        for y in range(3):
            if board[x][y] == "X" or board[x][y] == "O":
                continue
            else:
                pair = (x, y)  # tuple acc. to the task
                free.append(pair)
    return free


def victory_check(board, sign, towin):  # Checking if anyone has [towin] number of hits in a row (if not needed for winning algorithm, delete towin)

    # Checking for win in any triple
    for i in range(len(triples)):
        win = 0
        for j in range(3):
            x = triples[i][j][0] #Coordinates of the checked field
            y = triples[i][j][1]
            if board[x][y] == sign:
                win += 1
        if win == towin:
            return "win"
        else:
            win = 0
    return "next"

def win_block(board, xwin, owin): # if there are two identically checked fields in a row and the third field is empty, check the third one and win or block
    for i in range(len(triples)):
        xfld = 0
        ofld = 0
        for j in range(3):
            x = triples[i][j][0] #Coordinates of the checked field
            y = triples[i][j][1]
            if board[x][y] == "X":
                xfld += 1
            elif board[x][y] == "O":
                ofld += 1
        if xfld == xwin and ofld == owin: # Computer has 2 in the row, user has 0 - winning movement
            for j in range(3):
                x = triples[i][j][0]
                y = triples[i][j][1]
                if board[x][y] not in ["X", "O"]:
                    board[x][y] = "X"
                    return "ok"

def win_alg(board):
    # Implementation of winning algorithm acc. to:
    # https://swistak.codes/post/algorytmika-gier-kolko-i-krzyzyk/#strategia-wygrywania-w-kółko-i-krzyżyk
    # on the basis of https://onlinelibrary.wiley.com/doi/abs/10.1207/s15516709cog1704_3
    # 1. Winning move - if the computer has two checked fields in a row and the third field is empty, check the third one and win
    if win_block(board, 2, 0) == "ok":
        return "ok"
    # 2. Block - if the opponent has two checked fields in a row and the third field is empty, check the third one and block the opponent
    if win_block(board, 0, 2) == "ok":
        return "ok"


def draw_move(board):  # Computer's move & board update
    if win_alg(board) != "ok":
        from random import randrange
        free_fields = make_list_of_free_fields(board)
        if len(free_fields) != 0:
            comp_move = randrange(len(free_fields))
            field = free_fields[comp_move]  # tuple containing coordinates of computer move
            x = field[0]
            y = field[1]
            board[x][y] = "X"


# Initialization - empty board - list [row][column]
board = []
row = [x for x in range(1, 4)]
board.append(row)
row = [x for x in range(4, 7)]
board.append(row)
row = [x for x in range(7, 10)]
board.append(row)
display_board(board)

# List of all possible 3-field lines
triples = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
           ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)), ((0, 0), (1, 1), (2, 2)), ((2, 0), (1, 1), (0, 2)))

# Randomly selecting who starts
from random import randrange

who = randrange(2)
if who == 0:
    compsign = "X"
    print("Computer begins and plays with X")
    draw_move(board)  # First computer move is also random
else:
    compsign = "O"
    print("You begin and play with O")
display_board(board)

# Actual play
while True:
    # User move
    enter_move(board)
    display_board(board)
    if victory_check(board, "O", 3) == "win":
        print("You won")
        break
    print("Next computer move")
    # Computer move
    draw_move(board)
    display_board(board)
    if victory_check(board, "X", 3) == "win":
        print("Computer won")
        break
    if len(make_list_of_free_fields(board)) == 0:
        print("Draw")
        break



