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
def same_colour(stone1, stone2):
	return stone1.symbol == stone2.symbol

def remove_stones(coordinate_list, board, stones_played_list):
	for (row, col) in coordinate_list:
		board[row][col] = "+"
		stones_played_list.remove((row, col))
	return len(coordinate_list)

def check_liberties(row, col, board, stones_played_list):
	if board[row][col] == "+":
		return 0
	visited = [(row, col)]

	print("is_free = %s" % str(is_free(row, col, board, visited)))
	print("visited =", visited)
	num_removed = 0
	if is_free(row, col, board, visited) == False:
		num_removed = remove_stones(visited, board, stones_played_list)
		print("Num removed == %d" % num_removed)
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
	#print("New call")
	#print("visited = ", visited)
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

	def make_move(self, board):
		user_input = input("Ok, %s, place your stone.\n" % self.colour)
		if user_input.lower().find("pass") >= 0:
			return
		coordinates = str(user_input).split()
		print("user_input = \"%s\"" % user_input)
		print("coordinates = %s\n" % coordinates)
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
		print("Check")
		if self.colour == "black":
			print("Checking white liberties")
			for (row, col) in Player.white_stones_played:
				self.stones_capt += check_liberties(row, col, board, Player.white_stones_played)
			for (row, col) in Player.black_stones_played:
				self.stones_capt += check_liberties(row, col, board, Player.black_stones_played)
		else:
			print("Checking black liberties")
			for (row, col) in Player.black_stones_played:
				print("black_stones_played = ", Player.black_stones_played)
				self.stones_capt += check_liberties(row, col, board, Player.black_stones_played)
				print("stones_capt = %d" % self.stones_capt)
			for (row, col) in Player.white_stones_played:
				self.stones_capt += check_liberties(row, col, board, Player.white_stones_played)

black = Player("black")
white = Player("white")

print("\n\n\n")
print("Hello! Welcome to Go! Please start now.")

while black.black_stones_left > 0 and white.white_stones_left > 0:
	print_board(board)
	print("Player 1's turn. (%d stones left)" % black.black_stones_left)
	black.make_move(board)
	print_board(board)
	print("Player 2's turn. (%d stones left)" % white.white_stones_left)
	white.make_move(board)


while black.black_stones_left > 0:
	print_board(board)
	print("Player 1's turn. (%d stones left)" % black.black_stones_left)
	black.make_move(board)

while white.white_stones_left > 0:
	print_board(board)
	print("Player 2's turn. (%d stones left)" % white.whitestones_left)
	white.make_move(board)

print_board(board)

print("Game over!")
