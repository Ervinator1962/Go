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
			print("{:<4}".format(board[i][j]), end = "")
		print("\n")

class Player(object):
	def __init__(self, name):
		self.stones_capt = 0
		self.stones_left = 180
		self.colour = name
		if self.colour == "black":
			self.stones_left += 1
	def place_stone(self, board):
		user_input = input("Ok, %s, place your stone.\n" % self.colour)
		coordinates = user_input.split()
		row = int(coordinates[0])
		col = int(coordinates[1])
		while True:
			if row > 18 or row < 0 or col > 18 or col < 0:
				user_input = input("Invalid position, try again.\n")
				coordinates = user_input.split()
				row = int(coordinates[0])
				col = int(coordinates[1])
			elif board[row][col] == "O" or board[row][col] == "0":
				user_input = print("Position occupied, try again.\n")
				coordinates = user_input.split()
				row = int(coordinates[0])
				col = int(coordinates[1])
			else:
				print("Worked")
				if self.colour == "black":
					board[row][col] = "0"
				else:
					board[row][col] = "O"
				self.stones_left -= 1
				break

black = Player("black")
white = Player("white")

print("\n\n\n")
print("Hello! Welcome to Go! Please start now.")
while black.stones_left > 0:
	print_board(board)
	print("Player 1's turn.")
	black.place_stone(board)
	print_board(board)
	print("Player 2's turn.")
	white.place_stone(board)


