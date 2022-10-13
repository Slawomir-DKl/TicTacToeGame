def display_board(board):
    # The function accepts one parameter containing the board's current status
    # and prints it out to the console.

    #Board layout elements
    horiz = "+-------+-------+-------+"
    vert = "|       |       |       |"
    lft = "|  "
    btwn = "  |  "
    rght = "  |"

    #Printing the board
    print(horiz, vert, sep = '\n')
    print(lft, board[0][0], btwn, board[0][1], btwn, board[0][2], rght)
    print(vert, horiz, vert, sep = '\n')
    print(lft, board[1][0], btwn, board[1][1], btwn, board[1][2], rght)
    print(vert, horiz, vert, sep = '\n')
    print(lft, board[2][0], btwn, board[2][1], btwn, board[2][2], rght)
    print(vert, horiz, sep = '\n')

def enter_move(board):
    # The function accepts the board's current status, asks the user about their move,
    # checks the input, and updates the board according to the user's decision.

    #Asking user for input and checking it
    while True:
        try:
            move = int(input("Please enter number of square to put your mark: "))
            #Checking if number is > 0
            if move <= 0:
                chk = move/(move-move)
            #Calculating row and column @
            if move % 3 == 0:
                r = (move - move % 3)//3 - 1
                c = 2
            else:
                r = (move - move % 3)//3
                c = move % 3 - 1
            if board[r][c] == move: #Checking if the square is empty
                #Updating square
                board[r][c] = "O"
                break
            else:
                chk = nofunct
        except ValueError:
            print("It is not an integer!")
        except NameError:
            print("This square is occupied")
        except:
            print("The number is not in the range from 1 to 9")

def make_list_of_free_fields(board):
    # The function browses the board and builds a list of all the free squares;
    # the list consists of tuples, while each tuple is a pair of row and column numbers.

    free = []
    for x in range(3):
        for y in range(3):
            if board[x][y] == "X" or board[x][y] == "O":
                continue
            else:
                pair = (x, y)
                free.append(pair)
    return free

def victory_for(board, sign):
    # The function analyzes the board's status in order to check if
    # the player using 'O's or 'X's has won the game
    win = 0
    #Check for horizontal win
    for x in range(3):
        for y in range(3):
            if board[x][y] == sign:
                win += 1
        if win == 3:
            return "win"
        else:
            win = 0
    #Check for vertical win
    for x in range(3):
        for y in range(3):
            if board[y][x] == sign:
                win += 1
        if win == 3:
            return "win"
        else:
            win = 0
    #Check for 1st diagonal win
    for x in range(3):
        if board[x][x] == sign:
            win += 1
    if win == 3:
        return "win"
    else:
        win = 0
    #Check for 2nd diagonal win
    if board[0][2] == sign:
        win += 1
    if board[1][1] == sign:
        win += 1
    if board[2][0] == sign:
        win += 1
    if win == 3:
        return "win"
    return "next"
def draw_move(board):
    # The function draws the computer's move and updates the board.

    from random import randrange
    free_fields = make_list_of_free_fields(board)
    comp_move = randrange(len(free_fields))
    field = free_fields[comp_move] #tuple containing coordinates of computer move
    x = field[0]
    y = field[1]
    board[x][y] = "X"

#Initialization - empty board - list [row][column]
board = []
row = [x for x in range(1,4)]
board.append(row)
row = [x for x in range(4,7)]
board.append(row)
row = [x for x in range(7,10)]
board.append(row)
display_board(board)
print("Computer begins")
board[1][1] = "X" #first computer move
display_board(board)

while True:
    #User move
    enter_move(board)
    display_board(board)
    if victory_for(board, "O") == "win":
        print("You won")
        break
    print("Next computer move")
    #Computer move
    draw_move(board)
    display_board(board)
    if victory_for(board, "X") == "win":
        print("Computer won")
        break
    if len(make_list_of_free_fields(board)) == 0:
        print("Draw")
        break

