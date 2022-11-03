from random import randrange


def display_board(fnboard):  # Printing the current board

    # Board layout elements
    horiz = "+-----+-----+-----+"
    lft = "| "
    btwn = " | "
    rght = " |"

    # Printing the board
    print(horiz, sep='\n')
    print(lft, fnboard[0][0], btwn, fnboard[0][1], btwn, fnboard[0][2], rght)
    print(horiz, sep='\n')
    print(lft, fnboard[1][0], btwn, fnboard[1][1], btwn, fnboard[1][2], rght)
    print(horiz, sep='\n')
    print(lft, fnboard[2][0], btwn, fnboard[2][1], btwn, fnboard[2][2], rght)
    print(horiz, sep='\n')


def enter_move(fnboard):  # User's move & board update

    # Asking user for input and checking it
    while True:
        try:
            move = int(input("Please enter number of square to put your mark: "))
            # Checking if number is > 0
            if move <= 0:
                chk = move / (move - move)  # Generating ZeroDivisionError
            # Calculating row and column @
            if move % 3 == 0:
                x = (move - move % 3) // 3 - 1
                y = 2
            else:
                x = (move - move % 3) // 3
                y = move % 3 - 1
            if fnboard[x][y] == move:  # Checking if the square is empty
                # Updating square
                fnboard[x][y] = "O"
                break
            else:
                chk = nofunct  # non-existing function to generate the ValueError
        except ValueError:
            print("It is not an integer!")
        except NameError:
            print("This square is occupied. Enter the number of empty square.")
        except ZeroDivisionError:
            print("The number is not in the range from 1 to 9. Enter higher number.")
        except IndexError:
            print("The number is not in the range from 1 to 9. Enter lower number.")


def make_list_of_free_fields(fnboard):  # Building list of all the free squares

    free = []
    for x in range(3):
        for y in range(3):
            if fnboard[x][y] == "X" or fnboard[x][y] == "O":
                continue
            else:
                pair = (x, y)  # tuple acc. to the task
                free.append(pair)
    return free


def victory_check(fnboard, sign, towin):  # Checking if anyone has [towin] number of hits in a row (if not needed for
    # winning algorithm, delete towin)

    # Checking for win in any triple
    for triple in range(len(triples)):
        win = 0
        for field in range(3):
            x = triples[triple][field][0]  # Coordinates of the checked field
            y = triples[triple][field][1]
            if fnboard[x][y] == sign:
                win += 1
        if win == towin:
            return "win"
    return "next"


def count_xo(fnboard, triple):  # counting marked fields in a line

    xfld = 0
    ofld = 0
    for field in range(3):
        x = triples[triple][field][0]  # Coordinates of the checked field
        y = triples[triple][field][1]
        if fnboard[x][y] == "X":
            xfld += 1
        elif fnboard[x][y] == "O":
            ofld += 1
    return xfld, ofld


def win_block(fnboard, xwin, owin):  # if there are two identically checked fields in a row and the 3rd field is empty,
    # check the third one and win or block
    for triple in range(len(triples)):
        xfld, ofld = count_xo(fnboard, triple)
        if xfld == xwin and ofld == owin:  # Computer has 2 in the row, user has 0 - winning movement; computer has 0
            # in the row, user has 2 - blocking movement
            for field in range(3):
                x = triples[triple][field][0]
                y = triples[triple][field][1]
                if fnboard[x][y] not in ["X", "O"]:
                    fnboard[x][y] = "X"
                    return "ok"


def win_alg(fnboard):
    # Implementation of winning algorithm acc. to:
    # https://swistak.codes/post/algorytmika-gier-kolko-i-krzyzyk/#strategia-wygrywania-w-kółko-i-krzyżyk
    # on the basis of https://onlinelibrary.wiley.com/doi/abs/10.1207/s15516709cog1704_3
    # 1. Winning move - if the computer has two checked fields in a row and the third field is empty,
    # check the third one and win
    if win_block(fnboard, 2, 0) == "ok":
        return "ok"
    # 2. Block - if the opponent has two checked fields in a row and the third field is empty,
    # check the third one and block the opponent
    if win_block(fnboard, 0, 2) == "ok":
        return "ok"
    # 3. Do a fork - if you have two intersecting lines (horizontal, vertical, diagonal) with one your mark and with two
    # empty places AND if the intersection of the lines is empty, insert your mark in the intersection
    # (to create two possibilities to win in the next move)
    for triple in range(len(triples)):
        xfld, ofld = count_xo(fnboard, triple)
        if xfld == 1 and ofld == 0:  # first line with 1 computer mark and 0 user marks
            for interfield in range(len(intersections[triple])):  # checking all intersecting lines
                interline = intersections[triple][interfield]  # number of intersecting line to check
                xfldint, ofldint = count_xo(fnboard, interline)
                if xfldint == 1 and ofldint == 0:  # intersecting line with 1 computer mark and 0 user marks
                    for field in range(3):
                        for lcheckfield in range(3):
                            if triples[triple][field] == triples[interline][lcheckfield]:
                                x = triples[triple][field][0]  # Coordinates of the intersection
                                y = triples[triple][field][1]
                                if fnboard[x][y] not in ("O", "X"):
                                    fnboard[x][y] = "X"
                                    return "ok"

    # 4. Do a blocking fork if you have two intersecting lines (horizontal, vertical, diagonal) with one opponent mark
    # and with two empty places AND if the intersection of the lines is empty, then:
    # if the intersection would create two marks in a row for computer (that the opponent has to block
    # in his next move) - insert your mark in the intersection
    # else: if there is other empty place which would create two marks in a row for computer (that the opponent has
    # to block in his next move) - insert your mark in this empty place
    # else: insert your mark in the intersection (to block two possibilities to win for the opponent in the next move)

    for triple in range(len(triples)):
        xfld, ofld = count_xo(fnboard, triple)
        if xfld == 0 and ofld == 1:  # first line with 0 computer marks and 1 user mark
            print("first line 0/1", triple)
            for interfield in range(len(intersections[triple])):  # checking all intersecting lines
                interline = intersections[triple][interfield]  # number of intersecting line to check
                xfldint, ofldint = count_xo(fnboard, interline)
                if xfldint == 0 and ofldint == 1:  # intersecting line with 0 computer mark and 1 user marks
                    print("intersection 0/1", interfield, interline)
                    xint = 9
                    yint = 9
                    for field in range(3):  # Finding the intersection coordinates
                        for lcheckfield in range(3):
                            if triples[triple][field] == triples[interline][lcheckfield]:
                                print(field, lcheckfield)
                                xint = triples[triple][field][0]  # Coordinates of the intersection
                                yint = triples[triple][field][1]
                                if fnboard[xint][yint] not in ("O", "X"):  # TO DO - Y106701
                                    print(xint, yint)
                                    for chktriple in range(len(triples)):  # Checking if intersection creates two-in-a-row for comp.
                                        for chkfield in range(3):
                                            xchk = triples[chktriple][chkfield][0]
                                            ychk = triples[chktriple][chkfield][1]
                                            if xchk == xint and ychk == yint:
                                                xfldchk, ofldchk = count_xo(fnboard, chktriple)
                                                if xfldchk == 1 and ofldchk == 0:
                                                    fnboard[xint][yint] = "X"
                                                    return "ok"
                                    for sngltriple in range(len(triples)):  # Finding any line with single comp mark
                                        xsngl, osngl = count_xo(fnboard, sngltriple)
                                        if xsngl == 1 and osngl == 0:
                                            for snglfield in range(3):
                                                xsn = triples[sngltriple][snglfield][0]
                                                ysn = triples[sngltriple][snglfield][1]
                                                if fnboard[xsn][ysn] not in ("O", "X"):
                                                    fnboard[xsn][ysn] = "X"
                                                    return "ok"
                                    fnboard[xint][yint] = "X"  # Placing mark in the intersection
                                    return "ok"

    # 5. Use the center - if the center field is empty, insert your mark here
    if fnboard[1][1] not in ("O", "X"):
        fnboard[1][1] = "X"
        return "ok"

    # 6. Play the opposite corner - if the opponent has its mark in the corner and the opposite corner is empty,
    # insert your mark in the opposite corner
    corners = ((0, 0), (0, 2), (2, 0), (2, 2))
    opposite = ((2, 2), (2, 0), (0, 2), (0, 0))
    for corner in range(len(corners)):
        xcorn = corners[corner][0]
        ycorn = corners[corner][1]
        if fnboard[xcorn][ycorn] == "O":
            xopp = opposite[corner][0]
            yopp = opposite[corner][1]
            if fnboard[xopp][yopp] not in ("O", "X"):
                fnboard[xopp][yopp] = "X"
                return "ok"
    # 7. Occupy the empty corner - if there is an empty corner, insert your mark here
    for corner in range(len(corners)):
        xcorn = corners[corner][0]
        ycorn = corners[corner][1]
        if fnboard[xcorn][ycorn] not in ("O", "X"):
                fnboard[xcorn][ycorn] = "X"
                return "ok"
    # 8. Play on the empty side - if there is an empty side field, insert your mark here
    sides = ((0, 1), (1, 0), (1, 2), (2, 1))
    for side in range(len(sides)):
        xside = sides[side][0]
        yside = sides[side][1]
        if fnboard[xside][yside] not in ("O", "X"):
                fnboard[xside][yside] = "X"
                return "ok"
    return

def draw_move(fnboard):  # Computer's move & board update
    if win_alg(fnboard) != "ok":
        print("random move")
        from random import randrange
        free_fields = make_list_of_free_fields(fnboard)
        if len(free_fields) != 0:
            comp_move = randrange(len(free_fields))
            field = free_fields[comp_move]  # tuple containing coordinates of computer move
            x = field[0]
            y = field[1]
            fnboard[x][y] = "X"


# Initialization - empty board - list [row][column]
board = []
row = [x for x in range(1, 4)]
board.append(row)
row = [x for x in range(4, 7)]
board.append(row)
row = [x for x in range(7, 10)]
board.append(row)
display_board(board)

# List of all fields
fields = ((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2))

# List of all possible 3-field lines
triples = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
           ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)), ((0, 0), (1, 1), (2, 2)), ((2, 0), (1, 1), (0, 2)))
# All possible intersecting lines in relation to triples, i.e. line 0 intersects with lines 3, 4, 5, 6, 7 etc.
# Only one check of any line pair
intersections = ((3, 4, 5, 6, 7), (3, 4, 5, 6, 7), (3, 4, 5, 6, 7), (6, 7), (6, 7), (6, 7), (7,),
                 ())
# 4dev: to delete after finishing the program - without error management as it is for dev only
enter_initial = input("Enter Y if you want to enter initial positions: ")
if enter_initial == "Y":
    while True:
        fldno = int(input("Enter number of the field with computer X mark or enter 0 (zero) to stop entering: ")) - 1
        if fldno == -1:
            break
        else:
            selected_fld = fields[fldno]
            board[selected_fld[0]][selected_fld[1]] = "X"
            display_board(board)
    while True:
        fldno = int(input("Enter number of the field with user O mark or enter 0 (zero) to stop entering: ")) - 1
        if fldno == -1:
            break
        else:
            selected_fld = fields[fldno]
            board[selected_fld[0]][selected_fld[1]] = "O"
            display_board(board)
    select_starter = int(input("Select who begins. Enter 1 if computer or 0 if user"))
    if select_starter == 1:
        draw_move(board)  # First computer move is also algorythmised
else:  # here begins the part to leave in the final program
    # Randomly selecting who starts
    who = randrange(2)
    if who == 0:
        compsign = "X"
        print("Computer begins and plays with X")
        draw_move(board)  # First computer move is also algorythmised
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
