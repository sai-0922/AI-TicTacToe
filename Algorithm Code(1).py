# MODULES
import pygame, sys
import numpy as np

# initializes pygame
pygame.init()

# ---------
# CONSTANTS
# ---------
AI='X'
human='O'
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = 200
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55
# rgb: red green blue
RED = (255, 0, 0)
BG_COLOR = (255, 255, 200)
LINE_COLOR = (0, 0, 0)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# ------
# SCREEN
# ------
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption( 'TIC TAC TOE' )
screen.fill( BG_COLOR )

# -------------
# CONSOLE BOARD
# -------------
board = np.empty([BOARD_ROWS, BOARD_COLS],dtype=str)

# ---------
# FUNCTIONS
# ---------
def draw_lines():
	# 1 horizontal
	pygame.draw.line( screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH )
	# 2 horizontal
	pygame.draw.line( screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH )

	# 1 vertical
	pygame.draw.line( screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH )
	# 2 vertical
	pygame.draw.line( screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH )

def draw_figures():
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col] == human:
				pygame.draw.circle( screen, CIRCLE_COLOR, (int( col * SQUARE_SIZE + SQUARE_SIZE//2 ), int( row * SQUARE_SIZE + SQUARE_SIZE//2 )), CIRCLE_RADIUS, CIRCLE_WIDTH )
			if board[row][col] == AI:
				pygame.draw.line( screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
				pygame.draw.line( screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

def areEqual(a, b, c):
	return (a == b and b == c and a != '')


def checkwinner():
	winner = 'N'
	#Check horizontally
	for i in range(0, 3):
		if areEqual(board[i][0], board[i][1], board[i][2]):
			winner = board[i][0]

	#Check vertically
	for i in range(0, 3):
		if areEqual(board[0][i], board[1][i], board[2][i]):
			winner = board[0][i]

	#Check diagonally
	if areEqual(board[0][0], board[1][1], board[2][2]):
		winner = board[0][0]
	if areEqual(board[2][0], board[1][1], board[0][2]):
		winner = board[2][0]

	#Check for Tie
	emptyPlaces = 0;
	for i in range(0, 3):
		for j in range(0, 3):
			if board[i][j] == '':
				emptyPlaces += 1

	if winner == 'N' and emptyPlaces == 0:
	    return 'Tie'
	else:
	    return winner

def checkwinner1():
	winner = 'N'
	#Check horizontally
	for i in range(0, 3):
		if areEqual(board[i][0], board[i][1], board[i][2]):
			winner = board[i][0]
			posY = i * SQUARE_SIZE + SQUARE_SIZE // 2
			if winner == human:
				color = CIRCLE_COLOR
			elif winner == AI:
				color = CROSS_COLOR
			pygame.draw.line(screen, color, (15,posY), (WIDTH - 15, posY), 15)

	#Check vertically
	for i in range(0, 3):
		if areEqual(board[0][i], board[1][i], board[2][i]):
			winner = board[0][i]
			posX = i * SQUARE_SIZE + SQUARE_SIZE // 2
			if winner == human:
				color = CIRCLE_COLOR
			elif winner == AI:
				color = CROSS_COLOR
			pygame.draw.line(screen, color, (posX, 15), (posX, HEIGHT - 15), 15)

	#Check diagonally
	if areEqual(board[0][0], board[1][1], board[2][2]):
		winner = board[0][0]
		if winner == human:
			color = CIRCLE_COLOR
		elif winner == AI:
			color = CROSS_COLOR
		pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), 15)

	if areEqual(board[2][0], board[1][1], board[0][2]):
		winner = board[2][0]
		if winner == human:
			color = CIRCLE_COLOR
		elif winner == AI:
			color = CROSS_COLOR
		pygame.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), 15)


def mark_square(row, col, player):
	board[row][col] = player

def available_square(row, col):
	return board[row][col] == ''

def is_board_full():
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col] == '':
				return False
	return True

def displaywinner():
	Winner = checkwinner()
	font = pygame.font.Font('freesansbold.ttf', 100)
	if Winner != 'Tie':
		text = font.render(Winner + ' wins!!', True, RED, CIRCLE_COLOR)
	else:
		text = font.render('TIE Game', True, RED, CIRCLE_COLOR)
	textRect = text.get_rect()
	textRect.center = (SQUARE_SIZE + 100, SQUARE_SIZE + 100)
	screen.blit(text, textRect)

def bestmove():
	#In the turn of AI.
	bestScore = -2
	place = [4,]
	for i in range(BOARD_ROWS):
		for j in range(BOARD_COLS):
			# Is the spot available?
			if board[i][j] == '':
				board[i][j] = AI
				score = minimax(board, 0, False)
				board[i][j] = ''
				if score > bestScore:
					bestScore = score
					place = [i, j]

	if place[0] != 4:
		board[place[0]][place[1]] = AI


scores = {'X':1, 'O':-1, 'Tie':0}

def minimax(board, depth, maximizingTurn):
	_winner = checkwinner()
	if _winner != 'N':
		return scores[_winner]

	if maximizingTurn:
		bestScore = -2
		for i in range(0,3):
			for j in range(0,3):
				if board[i][j] == '':
					board[i][j] = AI
					score = minimax(board, depth + 1, False)
					board[i][j] = ''
					if score > bestScore:
						bestScore = score
		return bestScore

	if not maximizingTurn:
		bestScore = 2
		for i in range(0,3):
			for j in range(0,3):
				if board[i][j] == '':
					board[i][j] = human
					score = minimax(board, depth + 1, True)
					board[i][j] = ''
					if score < bestScore:
						bestScore = score
		return bestScore

# ---------
# VARIABLES
# ---------

# --------
# MAINLOOP
# --------
draw_lines()
CurrentPlayerIsHuman = True
run=True
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()


		if event.type == pygame.MOUSEBUTTONDOWN :
				if CurrentPlayerIsHuman:
					mouseX = event.pos[0]
					mouseY = event.pos[1]
					clicked_row = int(mouseY // SQUARE_SIZE)
					clicked_col = int(mouseX // SQUARE_SIZE)
					if available_square( clicked_row, clicked_col ):
						board[clicked_row][clicked_col] = human
						mark_square( clicked_row, clicked_col, human )
						draw_figures()
						CurrentPlayerIsHuman=False

				if not CurrentPlayerIsHuman:
					bestmove()
					draw_figures()
					CurrentPlayerIsHuman=True

				if checkwinner() != 'N':
					checkwinner1()
					displaywinner()

	pygame.display.update()
