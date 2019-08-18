import pygame

import entities


# constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 100
SMALL_BUTTON_SIZE = 80
MENU_TEXT_SIZE = 48
INSTRUCTIONS_TEXT_SIZE = 24
TRAINING_TEXT_SIZE = 36
BOARD_WIDTH = 8
BOARD_HEIGHT = 8
TILE_MARGIN = 4
TILE_SIZE = int((WINDOW_HEIGHT - (BOARD_HEIGHT + 1) * TILE_MARGIN) / BOARD_HEIGHT)
TILE_BUTTON_SIZE = 50

# colours
MENU_BACKGROUND_COLOUR = (50, 50, 50)
MENU_TEXT_COLOUR = (255, 255, 255)
INSTRUCTIONS_BACKGROUND_COLOUR = (50, 50, 50)
INSTRUCTIONS_TEXT_COLOUR = (255, 255, 255)
INSTRUCTIONS_BUTTON_COLOUR = (250, 250, 50)
TRAINING_BUTTON_COLOUR = (250, 80, 80)
TRAINING_BACKGROUND_COLOUR = (50, 50, 50)
TRAINING_TEXT_COLOUR = (255, 255, 255)
EMPTY_TILE_COLOUR = (255, 255, 255)
OBSTACLE_TILE_COLOUR = (250, 100, 100)
REWARD_TILE_COLOUR = (250, 250, 100)

# initiate pygame, set the window title, and create the background
pygame.init()
pygame.display.set_caption("Q Learning Game")
background = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

def menu():
	# font for menu
	font = pygame.font.SysFont('Comic Sans MS', MENU_TEXT_SIZE)

	# the buttons
	train_button = entities.Button((WINDOW_WIDTH - BUTTON_WIDTH) / 2, WINDOW_HEIGHT / 2, BUTTON_WIDTH, BUTTON_HEIGHT)
	instructions_button = entities.Button(40, 40, SMALL_BUTTON_SIZE, SMALL_BUTTON_SIZE)

	# loop variables
	in_menu = True
	choice = None

	while in_menu:
		# refresh background
		background.fill(MENU_BACKGROUND_COLOUR)

		# check for user mouse input
		for event in pygame.event.get():
			if event.type == pygame.QUIT:	# red 'x' at top of window clicked
				choice = 'exit'
				in_menu = False
			if event.type == pygame.MOUSEBUTTONDOWN:	# mouse click
				mouse_position = event.pos
				if train_button.collidepoint(mouse_position):
					choice = 'train'
					in_menu = False
				if instructions_button.collidepoint(mouse_position):
					choice = 'instructions'
					in_menu = False

		# draw the buttons
		pygame.draw.rect(background, TRAINING_BUTTON_COLOUR, train_button)
		pygame.draw.rect(background, INSTRUCTIONS_BUTTON_COLOUR, instructions_button)

		# draw the text
		display_text(font, "Press the yellow button for instructions,",\
			(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - BUTTON_HEIGHT), MENU_TEXT_COLOUR, centered = True)
		display_text(font, "or the red button to train!",\
			(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - BUTTON_HEIGHT / 2), MENU_TEXT_COLOUR, centered = True)

		# update the window
		pygame.display.update()

	return choice


def instructions():
	# font for instructions
	font = pygame.font.SysFont('Comic Sans MS', INSTRUCTIONS_TEXT_SIZE)

	in_instructions = True

	while in_instructions:
		# refresh background
		background.fill(INSTRUCTIONS_BACKGROUND_COLOUR)

		# check for user mouse input
		for event in pygame.event.get():
			if event.type == pygame.QUIT:	# red 'x' at top of window clicked
				in_instructions = False

		# check if ESC pressed
		keys = pygame.key.get_pressed()
		if keys[pygame.K_ESCAPE]:
			in_instructions = False

		# display the instructions
		display_text(font, "Rules/Objectives:", (50, 50 + INSTRUCTIONS_TEXT_SIZE), INSTRUCTIONS_TEXT_COLOUR)
		display_text(font, "   -  The white squares are safe, the red squares are obstacles",\
			(50, 50 + 2 * INSTRUCTIONS_TEXT_SIZE), INSTRUCTIONS_TEXT_COLOUR)
		display_text(font, "   -  The small black square is trying to get to a yellow square",\
			(50, 50 + 3 * INSTRUCTIONS_TEXT_SIZE), INSTRUCTIONS_TEXT_COLOUR)
		display_text(font, "Controls:", (50, 50 + 4 * INSTRUCTIONS_TEXT_SIZE), INSTRUCTIONS_TEXT_COLOUR)
		display_text(font, "   -  To place obstacles, press the red square on the side and then click a square on the grid",\
			(50, 50 + 5 * INSTRUCTIONS_TEXT_SIZE), INSTRUCTIONS_TEXT_COLOUR)
		display_text(font, "   -  To replace obstacles, press the white square on the side and click on an obstacle",\
			(50, 50 + 6 * INSTRUCTIONS_TEXT_SIZE), INSTRUCTIONS_TEXT_COLOUR)
		display_text(font, "   -  To place a reward, press the yellow square on the side and then click a square on the grid",\
			(50, 50 + 7 * INSTRUCTIONS_TEXT_SIZE), INSTRUCTIONS_TEXT_COLOUR)
		display_text(font, "   -  Press ENTER to start the training once you have made the course",\
			(50, 50 + 8 * INSTRUCTIONS_TEXT_SIZE), INSTRUCTIONS_TEXT_COLOUR)
		display_text(font, "   -  Press SPACE to toggle the decreasing random move percentage",\
			(50, 50 + 9 * INSTRUCTIONS_TEXT_SIZE), INSTRUCTIONS_TEXT_COLOUR)
		display_text(font, "   -  Press RIGHT ARROW to increase the speed up the training",\
			(50, 50 + 10 * INSTRUCTIONS_TEXT_SIZE), INSTRUCTIONS_TEXT_COLOUR)
		display_text(font, "   -  Press LEFT ARROW to decrease the speed of the training",\
			(50, 50 + 11 * INSTRUCTIONS_TEXT_SIZE), INSTRUCTIONS_TEXT_COLOUR)
		display_text(font, "   -  Press ESC to exit the training (training progress and maze will be lost)",\
			(50, 50 + 12 * INSTRUCTIONS_TEXT_SIZE), INSTRUCTIONS_TEXT_COLOUR)
		display_text(font, "Press ESC to go to menu",\
			(50, 50 + 14 * INSTRUCTIONS_TEXT_SIZE), INSTRUCTIONS_TEXT_COLOUR)

		# update the window
		pygame.display.update()


def train():
	# font for training
	font = pygame.font.SysFont('Comic Sans MS', TRAINING_TEXT_SIZE)

	# define a base and max moves-per-second (MPS)
	MPS = 20
	MIN_MPS = MPS
	MAX_MPS = MPS * 2 ** 3

	# entities for training
	board = entities.Board(BOARD_WIDTH, BOARD_HEIGHT)
	for row in range(BOARD_HEIGHT):
		for column in range(BOARD_WIDTH):
			board.add_tile(entities.Tile(column * TILE_SIZE + TILE_MARGIN * column + TILE_MARGIN,\
				row * TILE_SIZE + TILE_MARGIN * row + TILE_MARGIN, TILE_SIZE, column, row, 'empty'))
	empty_button = entities.Button(WINDOW_WIDTH - 1.1 * TILE_BUTTON_SIZE,\
		TILE_BUTTON_SIZE, TILE_BUTTON_SIZE, TILE_BUTTON_SIZE)
	obstacle_button = entities.Button(WINDOW_WIDTH - 1.1 * TILE_BUTTON_SIZE,\
		TILE_BUTTON_SIZE + 1.5 * TILE_BUTTON_SIZE, TILE_BUTTON_SIZE, TILE_BUTTON_SIZE)
	reward_button = entities.Button(WINDOW_WIDTH - 1.1 * TILE_BUTTON_SIZE,\
		TILE_BUTTON_SIZE + 3 * TILE_BUTTON_SIZE, TILE_BUTTON_SIZE, TILE_BUTTON_SIZE)

	# loop variables
	in_training = True
	started = False
	decrease_randomness = True
	tile_choice = 'empty'
	current_key_pressed = None

	while in_training:
		# refresh background
		background.fill(TRAINING_BACKGROUND_COLOUR)

		# check for user mouse input
		for event in pygame.event.get():
			if event.type == pygame.QUIT:	# red 'x' at top of window clicked
				in_training = False
			if event.type == pygame.MOUSEBUTTONDOWN:	# mouse click
				mouse_position = event.pos
				if empty_button.collidepoint(mouse_position):
					tile_choice = 'empty'
				elif obstacle_button.collidepoint(mouse_position):
					tile_choice = 'obstacle'
				elif reward_button.collidepoint(mouse_position):
					tile_choice = 'reward'
				elif board.tile_clicked(mouse_position):
					board.change_tile_type(tile_choice)

		# handle key inputs from either both, or just one player
		keys = pygame.key.get_pressed()
		if keys[pygame.K_ESCAPE]:
			in_training = False
		elif keys[pygame.K_RETURN]:
			started = True
		elif keys[pygame.K_SPACE] and current_key_pressed != pygame.K_SPACE:
			decrease_randomness = False if decrease_randomness else True
			current_key_pressed = pygame.K_SPACE
		elif keys[pygame.K_RIGHT] and current_key_pressed != pygame.K_RIGHT:
			if MPS < MAX_MPS:
				MPS *= 2
			current_key_pressed = pygame.K_RIGHT
		elif keys[pygame.K_LEFT] and current_key_pressed != pygame.K_LEFT:
			if MPS > MIN_MPS:
				MPS /= 2
			current_key_pressed = pygame.K_LEFT
		else:
			current_key_pressed = None

		# draw the board
		board.draw_board(background)

		# update the board
		board.update(started, decrease_randomness)

		# display the buttons
		pygame.draw.rect(background, EMPTY_TILE_COLOUR, empty_button)
		pygame.draw.rect(background, OBSTACLE_TILE_COLOUR, obstacle_button)
		pygame.draw.rect(background, REWARD_TILE_COLOUR, reward_button)

		# display the % random moves and fast-forward speed
		display_text(font, str(abs(round(board.player.epsilon * 100, 1))) + "% Random",\
			(WINDOW_WIDTH - 100, WINDOW_HEIGHT - 50 - TRAINING_TEXT_SIZE), TRAINING_TEXT_COLOUR, centered = True)
		display_text(font, u"\u00d7" + str(MPS / MIN_MPS), (WINDOW_WIDTH - 50, WINDOW_HEIGHT - 50),\
			TRAINING_TEXT_COLOUR, centered = True)

		# update the window
		pygame.display.update()

		# wait to draw the next frame to ensure this frame is visible
		pygame.time.wait(int(1000 / MPS))



# display text without a hassle
def display_text(font, text, position, colour, centered = False):
	# get the textview to do some positioning if needed
	text_view = font.render(text, True, colour)
	if position == 'center':	# position in center of screen
		background.blit(text_view, ((WINDOW_WIDTH - text_view.get_rect().width) / 2, WINDOW_HEIGHT / 2))
	elif not centered:	# position the top left according to the position argument
		background.blit(text_view, position)
	else:	# position the center at the position argument
		background.blit(text_view, (position[0] - text_view.get_rect().width / 2,\
			position[1] - text_view.get_rect().height / 2))


if __name__ == "__main__":
	while True:
		choice = menu()
		
		if choice == 'train':
			train()
		elif choice == 'instructions':
			instructions()
		elif choice == 'exit':
			break

	pygame.quit()





