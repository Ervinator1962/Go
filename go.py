# extra row for x-axis coordinates
game_board = [["+" for x in range(20)] for y in range(20)]
for i in range(len(game_board) - 1):
    game_board[i][19] = i
for i in range(len(game_board[0]) - 1):
    game_board[19][i] = i
game_board[19][19] = ""


def print_board(board):
    print("\n\n\n")
    for i in range(len(board)):
        for j in range(len(board[0])):
            if type(board[i][j]) is Stone:
                print("{:<4}".format(board[i][j].symbol), end="")
            else:
                print("{:<4}".format(board[i][j]), end="")
        print("\n")


"""
def check_boundaries(board):
    print("Checking boundaries")
    for row in range(19):
        for col in range(19):
            if type(board[row][col]) is Stone:
                visited = [(row,col)]
                input("Next src: %d %d" % (row, col))
                is_free(row, col, board, visited)
                for stone in visited:
                    print(stone)
"""


def on_board(pos):
    return 0 <= pos[0] <= 18 and 0 <= pos[1] <= 18


def is_stone(pos, board):
    assert on_board(pos)
    return type(board[pos[0]][pos[1]]) is Stone


def same_colour(pos1, pos2, board):
    assert is_stone(pos1, board), "pos1 is not a valid stone"
    assert is_stone(pos2, board), "pos2 is not a valid stone"
    return board[pos1[0]][pos1[1]].symbol == board[pos2[0]][pos2[1]].symbol


def remove_stones(coordinate_list, board, stones_played_list):
    #TODO: fix stones_played_list
    for (row, col) in coordinate_list:
        # indicate the current round's captured stones with '.'
        board[row][col] = "."
        stones_played_list.remove((row, col))
    return len(coordinate_list)


# remove the "."'s that indicate the last round's captured positions
def remove_capture_indicators(board):
    for i in range(19):
        for j in range(19):
            if board[i][j] == ".":
                board[i][j] = "+"


# TODO: Add visited to parent function of check liberties
# TODO: Edit, cannot do above since need new visited list containing objects to delete every new call to function.
# TODO: Check stones_played_list
def check_liberties(row, col, board, stones_played_list):
    # print("New src = %d %d" % (row, col))
    if is_stone((row, col), board) is False:
        return 0
    # TODO: change assignment operator to .append
    visited = [(row, col)]
    has_liberties = is_free(row, col, board, visited)
    # print("is_free = %s" % str(has_liberties))
    # print("visited =", visited)
    num_removed = 0
    if has_liberties == False:
        # print("is_free must be false: is_free = %s" % str(has_liberties))
        num_removed = remove_stones(visited, board, stones_played_list)
    # print("Num removed == %d" % num_removed)
    return num_removed


"""
    visited = [(row, col)]
    num_edges = is_free(row, col, board, visited)
    num_liberties = 0
    for (row, col) in visited:
        num_liberties += board[row][col].num_liberties
    num_liberties -= num_edges
    if num_edges == 0:
        print("Captured")
    else:
        print("Not Captured")
"""


def is_free(row, col, board, visited):
    has_liberties = False
    # print("New call")
    # print("visited = ", visited)
    pos_above = (row - 1, col)
    pos_below = (row + 1, col)
    pos_left = (row, col - 1)
    pos_right = (row, col + 1)
    positions = [pos_above, pos_below, pos_left, pos_right]

    # remove positions not on board, i.e. all pos in list positions will be valid thereafter
    for pos in positions:
        if on_board(pos) is False:
            positions.remove(pos)
        elif is_stone(pos, board) is False:
            # if pos is on the board and does not hold stone then it is a liberty
            has_liberties = True
            return has_liberties

    for pos in positions:
        if same_colour((row, col), pos, board) and pos not in visited:
            visited.append(pos)
            # input("pos: %d %d" % (row - 1, col))
            has_liberties = is_free(pos[0], pos[1], board, visited)
            if has_liberties is True:
                break

    return has_liberties


"""
def is_free(row, col, board, visited):
    has_liberties = False
    #print("New call")
    #print("visited = ", visited)
    if has_liberties == False:
        if row + 1 <= 18 and (row + 1, col) not in visited:
            if type(board[row + 1][col]) is Stone:
                if same_colour(board[row + 1][col], board[row][col]):
                    visited.append((row + 1, col)) 
                    #input("pos: %d %d" % (row + 1, col))
                    has_liberties = is_free(row + 1, col, board, visited)
            else:
                has_liberties = True
        if row - 1 >= 0 and (row - 1, col) not in visited:
            if type(board[row - 1][col]) is Stone:
                if same_colour(board[row - 1][col], board[row][col]):
                    visited.append((row - 1, col)) 
                    #input("pos: %d %d" % (row - 1, col))
                    has_liberties = is_free(row - 1, col, board, visited)
            else:
                has_liberties = True
        if col + 1 <= 18 and (row, col + 1) not in visited:
            if type(board[row][col + 1]) is Stone:
                if same_colour(board[row][col + 1], board[row][col]):
                    visited.append((row, col + 1))
                    #input("pos: %d %d" % (row, col + 1))
                    has_liberties = is_free(row, col + 1, board, visited)
            else:
                has_liberties = True
        if col - 1 >= 0 and (row, col - 1) not in visited:
            if type(board[row][col - 1]) is Stone:
                if same_colour(board[row][col - 1], board[row][col]):
                    visited.append((row, col - 1))
                    #input("pos: %d %d" % (row, col - 1))
                    has_liberties = is_free(row, col - 1, board, visited)
            else:
                has_liberties = True
    return has_liberties
"""


class Stone(object):
    def __init__(self, symbol):
        self.symbol = symbol


def create_stone_list(num_stones, symbol):
    stones = []
    for i in range(num_stones):
        stone = Stone(str(symbol))
        stones.append(stone)
    return stones


class Player(object):
    white_stones_played = []
    black_stones_played = []
    white_stones_left = 180
    black_stones_left = 181

    def __init__(self, name):
        self.stones_capt = 0
        self.colour = name
        self.stones = []
        if self.colour == "black":
            self.stones = create_stone_list(181, "@")
        else:
            self.stones = create_stone_list(180, "O")

    def show_captured(self):
        print(self.stones_capt)

    def make_move(self, board):
        user_input = input("Ok, %s, place your stone.\n" % self.colour)
        if user_input.lower().find("pass") >= 0:
            return
        coordinates = user_input.split()
        # print("user_input = \"%s\"" % user_input)
        # print("coordinates = %s\n" % coordinates)
        row = int(coordinates[0])
        col = int(coordinates[1])
        while True:
            if row > 18 or row < 0 or col > 18 or col < 0:
                user_input = input("Invalid position, try again.\n")
                coordinates = user_input.split()
                row = int(coordinates[0])
                col = int(coordinates[1])
            elif type(board[row][col]) is Stone:
                user_input = input("Position occupied, try again.\n")
                coordinates = user_input.split()
                row = int(coordinates[0])
                col = int(coordinates[1])
            else:
                board[row][col] = self.stones.pop(0)
                board[row][col].set_liberties(row, col)
                if self.colour == "black":
                    Player.black_stones_played.append((row, col))
                else:
                    Player.white_stones_played.append((row, col))
                print(board[row][col].num_liberties)
                if self.colour == "black":
                    Player.black_stones_left -= 1
                else:
                    Player.white_stones_left -= 1
                break
        remove_capture_indicators(board)
        # print("Check")
        if self.colour == "black":
            # print("Checking white liberties")
            for (row, col) in Player.white_stones_played:
                self.stones_capt += check_liberties(row, col, board, Player.white_stones_played)
            # print("Checking black liberties")
            for (row, col) in Player.black_stones_played:
                self.stones_capt += check_liberties(row, col, board, Player.black_stones_played)
        else:
            # print("Checking black liberties")
            for (row, col) in Player.black_stones_played:
                self.stones_capt += check_liberties(row, col, board, Player.black_stones_played)
            # print("Checking white liberties")
            for (row, col) in Player.white_stones_played:
                self.stones_capt += check_liberties(row, col, board, Player.white_stones_played)
# print("white stones = ", Player.white_stones_played)
# print("black stones = ", Player.black_stones_played)


black = Player("black")
white = Player("white")

print("\n\n\n")
print("Hello! Welcome to Go! Please start now.")

while black.black_stones_left > 0 and white.white_stones_left > 0:
    if __debug__:
        print_board(game_board)
    print("Player 1's turn. (%d stones left, %d stone(s) captured)" % (black.black_stones_left, black.stones_capt))
    black.make_move(game_board)
    if __debug__:
        print_board(game_board)
    print("Player 2's turn. (%d stones left, %d stone(s) captured)" % (white.white_stones_left, white.stones_capt))
    white.make_move(game_board)

while black.black_stones_left > 0:
    if __debug__:
        print_board(game_board)
    print("Player 1's turn. (%d stones left, %d stone(s) captured)" % (black.black_stones_left, black.stones_capt))
    black.make_move(game_board)

while white.white_stones_left > 0:
    if __debug__:
        print_board(game_board)
    print("Player 2's turn. (%d stones left, %d stone(s) captured)" % (white.white_stones_left, white.stones_capt))
    white.make_move(game_board)

if __debug__:
    print_board(game_board)

if black.stones_capt == white.stones_capt:
    print("Congratulations, you have tied")
elif black.stones_capt > white.stones_capt:
    print("Congratulations %s, you won!" % "PLayer 1")
else:
    print("Congratulations %s, you won!" % "Player 2")

print("Game over!")
