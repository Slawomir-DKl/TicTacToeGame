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


def victory_check(fnboard, sign):  # Checking if anyone has 3 hits in a row

    # Checking for win in any triple
    for triple in range(len(triples)):
        win = 0
        for field in range(3):
            x = triples[triple][field][0]  # Coordinates of the checked field
            y = triples[triple][field][1]
            if fnboard[x][y] == sign:
                win += 1
        if win == 3:
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


def win_alg(fnboard):  # Implementation of winning algorithm

    # 1. Win
    # If there is a row, column, or diagonal with two of my pieces and o blank space,
    # Then ploy the blank space (thus winning the game).
    if win_block(fnboard, 2, 0) == "ok":
        return "ok"

    # 2. Block
    # If there is a row, column, or diagonal with two of my opponent’s pieces and a blank space,
    # Then play the blank space (thus blocking a potential win for my opponent).
    if win_block(fnboard, 0, 2) == "ok":
        return "ok"

    # 3. Fork
    # If there are two intersecting rows, columns, or diagonals with one of my pieces and two blonks, and
    # If the intersecting space is empty,
    # Then move to the intersecting space (thus creating two woys to win on my next turn).
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

    # 4. Block Fork
    # If there are two intersecting rows, columns, or diagonals with one of my opponent’s pieces ond two blanks, and
    # If the intersecting space is empty,
    # Then
        # If there is an empty location that creates a two-in-o-row for me
            # (thus forcing my opponent to block rather than fork),
        # Then move to the location.
        # Else move to the Intersection space (thus occupying the location that my opponent could use to fork).
    xempty = []
    yempty = []
    for triple in range(len(triples)):
        xfld, ofld = count_xo(fnboard, triple)
        if xfld == 0 and ofld == 1:  # first line with 0 computer marks and 1 user mark
            for interfield in range(len(intersections[triple])):  # checking all intersecting lines
                interline = intersections[triple][interfield]  # number of intersecting line to check
                xfldint, ofldint = count_xo(fnboard, interline)
                if xfldint == 0 and ofldint == 1:  # intersecting line with 0 computer mark and 1 user marks
                    for field in range(3):  # Finding the intersection coordinates
                        for lcheckfield in range(3):
                            xint = triples[triple][field][0]  # Coordinates of the intersection
                            yint = triples[triple][field][1]
                            if triples[triple][field] == triples[interline][lcheckfield]:
                                if fnboard[xint][yint] not in ("O", "X"):
                                    for chktriple in range(6):  # Chk if inters. creates 2-in-a-row for X (excl. diag.)
                                        for chkfield in range(3):
                                            xchk = triples[chktriple][chkfield][0]
                                            ychk = triples[chktriple][chkfield][1]
                                            if xchk == xint and ychk == yint:
                                                xfldchk, ofldchk = count_xo(fnboard, chktriple)
                                                if xfldchk == 1 and ofldchk == 0:
                                                    fnboard[xint][yint] = "X"
                                                    return "ok"
                                    xempty.append(xint)
                                    yempty.append(yint)
    if len(xempty) > 0:  # Some empty intersections detected, but without 2-in-a-row for X
        sing = []  # Finding any line with single comp mark
        singtrip = []
        for sngltriple in range(6):  # To exclude diagonals - it would create fork possibility for opponent
            xsngl, osngl = count_xo(fnboard, sngltriple)
            if xsngl == 1 and osngl == 0:
                for snglfield in range(3):
                    xsn = triples[sngltriple][snglfield][0]
                    ysn = triples[sngltriple][snglfield][1]
                    if fnboard[xsn][ysn] not in ("O", "X"):
                        sing.append(snglfield)
                        singtrip.append(sngltriple)
        if len(sing) > 0:
            selected_sing = randrange(len(sing))
            xsn = triples[singtrip[selected_sing]][sing[selected_sing]][0]
            ysn = triples[singtrip[selected_sing]][sing[selected_sing]][1]
            fnboard[xsn][ysn] = "X"
            return "ok"
        selected_empty = randrange(len(xempty))  # Placing mark in the empty intersection
        xint = xempty[selected_empty]
        yint = yempty[selected_empty]
        fnboard[xint][yint] = "X"
        return "ok"

    # 5. Play Center
    # If the center is blank,
    # Then play the center.
    if fnboard[1][1] not in ("O", "X"):
        fnboard[1][1] = "X"
        return "ok"

    # 6. Play Opposite Corner
    # If my opponent is in a corner, and
    # If the opposite corner is empty,
    # Then play the opposite corner.
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

    # 7. Ploy Empty Corner
    # If there is an empty corner,
    # Then move to an empty corner.
    corn = []
    for corner in range(len(corners)):
        xcorn = corners[corner][0]
        ycorn = corners[corner][1]
        if fnboard[xcorn][ycorn] not in ("O", "X"):
            corn.append(corner)
    if len(corn) > 0:
        selected_corn = randrange(len(corn))
        xcorn = corners[corn[selected_corn]][0]
        ycorn = corners[corn[selected_corn]][1]
        fnboard[xcorn][ycorn] = "X"
        return "ok"

    # 8. Play Empty Side
    # If there is an empty side,
    # Then move to an empty side.
    sides = ((0, 1), (1, 0), (1, 2), (2, 1))
    sid = []
    for side in range(len(sides)):
        xside = sides[side][0]
        yside = sides[side][1]
        if fnboard[xside][yside] not in ("O", "X"):
            sid.append(side)
    if len(sid) > 0:
        selected_side = randrange(len(sid))
        xside = sides[sid[selected_side]][0]
        yside = sides[sid[selected_side]][1]
        fnboard[xside][yside] = "X"
        return "ok"


def draw_move(fnboard):  # Computer's move & board update
    random_number = randrange(4)
    if random_number < lvl - 1:
        win_alg(fnboard)
        print("This is a winning algorithm")
    else:
        print("This is a random move")
        free_fields = make_list_of_free_fields(fnboard)
        if len(free_fields) != 0:
            comp_move = randrange(len(free_fields))
            field = free_fields[comp_move]  # tuple containing coordinates of computer move
            x = field[0]
            y = field[1]
            fnboard[x][y] = "X"


# Start: level selection
while True:
    try:
        lvl = int(input("Please select level from 1 (easiest, random) to 5 (hardest): "))
        # Checking if number is in range
        if lvl < 1 or lvl > 5:
            chk = lvl / (lvl - lvl)  # Generating ZeroDivisionError
        else:
            break
    except ValueError:
        print("It is not an integer!")
    except ZeroDivisionError:
        print("The number is not in the range from 1 to 5. Enter it again.")

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

# Randomly selecting who starts
who = randrange(2)
if who == 0:
    compsign = "X"
    print("Computer begins and plays with X")
    draw_move(board)
else:
    compsign = "O"
    print("You begin and play with O")
display_board(board)

# Actual play

while True:
    # User move
    enter_move(board)
    display_board(board)
    if victory_check(board, "O") == "win":
        print("You won")
        break
    print("Next computer move")
    # Computer move
    draw_move(board)
    display_board(board)
    if victory_check(board, "X") == "win":
        print("Computer won")
        break
    if len(make_list_of_free_fields(board)) == 0:
        print("Draw")
        break
