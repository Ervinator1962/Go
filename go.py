#extra row for x-axis coordinates
board = [["+" for x in range(20)] for y in range(20)]
for i in range(len(board) - 1):
	board[i][19] = i
for i in range(len(board[0]) - 1):
	board[19][i] = i
board[19][19] = ""

def print_board(board):
	print("\n\n\n")
	for i in range(len(board)):
		for j in range(len(board[0])):
			if type(board[i][j]) is Stone:
				print("{:<4}".format(board[i][j].symbol), end = "")				
			else:
				print("{:<4}".format(board[i][j]), end = "")
		print("\n")

def check_boundaries(board):
	for row in range(19):
		for col in range(19):
			if type(board[row][col]) is Stone:

def find_connections(row, col, board, visited):
	if (row + 1, col) is not in visited and type(board[row + 1][col]) is Stone:
		visited += (row + 1, col) 
		find_connections(row + 1, col, board, visited)
	elif (row - 1, col) is not in visited and type(board[row - 1][col]) is Stone:
		visited += (row - 1, col) 
	elif (row, col + 1) is not in visited and type(board[row][col + 1]) is Stone:
		visited += (row, col + 1) 
	else (row, col - 1) is not in visited and type(board[row][col - 1]) is Stone:
		visited += (row, col - 1) 

class Stone(object):
	def __init__(self, symbol):
		self.symbol = symbol
		self.num_liberties = 0
	def set_liberties(self, row, col):
		if row == 0 and col == 0 or row == 0 and col == 18 or \
		row == 18 and col == 0 or row == 18 and col == 18:
			self.num_liberties = 2 
		elif row == 0 or col == 0 or row == 18 or col == 18:
			self.num_liberties = 3
		else:
			self.num_liberties = 4

def create_stone_list(num_stones, symbol):
	stones = []
	for i in range(num_stones):
		stone = Stone(str(symbol))
		stones.append(stone)
	return stones

class Player(object):
	def __init__(self, name):
		self.stones_capt = 0
		self.stones_left = 180
		self.colour = name
		self.stones = []
		if self.colour == "black":
			self.stones = create_stone_list(181, "@")
			self.stones_left += 1
		else:
			self.stones = create_stone_list(180, "O")

	def make_move(self, board):
		user_input = input("Ok, %s, place your stone.\n" % self.colour)
		if user_input.lower().find("pass") >= 0:
			return
		coordinates = user_input.split()
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
				if self.colour == "black":
					board[row][col] = self.stones.pop(0)
					board[row][col].set_liberties(row, col)
				else:
					board[row][col] = self.stones.pop(0)
					board[row][col].set_liberties(row, col)
				print(board[row][col].num_liberties)
				self.stones_left -= 1
				break

black = Player("black")
white = Player("white")

print("\n\n\n")
print("Hello! Welcome to Go! Please start now.")

while black.stones_left > 0 and white.stones_left > 0:
	print_board(board)
	print("Player 1's turn. (%d stones left)" % black.stones_left)
	black.make_move(board)
	print_board(board)
	print("Player 2's turn. (%d stones left)" % white.stones_left)
	white.make_move(board)

while black.stones_left > 0:
	print_board(board)
	print("Player 1's turn. (%d stones left)" % black.stones_left)
	black.make_move(board)

while white.stones_left > 0:
	print_board(board)
	print("Player 2's turn. (%d stones left)" % white.stones_left)
	white.make_move(board)

print_board(board)

print("Game over!")
