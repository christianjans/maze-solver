import pygame
import random
import numpy as np


class Button(pygame.Rect):
	# perhaps add more functionality later
	def __init__(self, x, y, width, height):
		super().__init__(x, y, width, height)

class Board():
	PLAYER_SIZE = 10

	def __init__(self, board_width, board_height):
		# save the number of rows and columns in the board
		self.rows = board_height
		self.columns = board_width

		# variables for the tiles on the board
		self.tiles = [[0] * self.columns for i in range(self.rows)]
		self.clicked_tile = None

		# make the player for the board
		self.player = Player(0, 0, self.PLAYER_SIZE, self.columns, self.rows)

	def add_tile(self, tile):
		# add a tile to the tile list at a the tile's spot on the board
		self.tiles[tile.board_y][tile.board_x] = tile

	def tile_clicked(self, position):
		# loop through the tiles to see if they were clicked
		for row in range(self.rows):
			for column in range(self.columns):
				tile = self.tiles[row][column]
				if tile.collidepoint(position):
					# a tile was clicked, save that tile
					self.clicked_tile = tile
					return True
		# no tiles were clicked
		return False

	def change_tile_type(self, tile_type):
		# change the currently selected tile to the argument's tile type
		self.clicked_tile.change_type(tile_type)

	def draw_board(self, background):
		# draw the board onto the background
		for row in range(self.rows):
			for column in range(self.columns):
				# get the tile at this row and column
				tile = self.tiles[row][column]
				# draw the tile onto the background
				pygame.draw.rect(background, tile.colour, tile)

		# draw the player onto the background
		pygame.draw.rect(background, self.player.PLAYER_COLOUR, self.player)

	def update(self, started, decrease_randomness):
		# move the player if the user has started the training
		if started:
			self.player.move(decrease_randomness)

		# get the tile the player is currently on
		player_tile = self.tiles[self.player.board_y][self.player.board_x]

		# check for collision
		if player_tile.tile_type == 'empty':
			# give the player a small reward for not running into an obstacle
			self.player.update_table(0.01)
		elif player_tile.tile_type == 'obstacle':
			# give the player a negative reward for running into an obstacle
			self.player.update_table(-10)
		elif player_tile.tile_type == 'reward':
			# reward the player for reaching the reward
			self.player.update_table(10)
			# bring the player back to its starting position
			self.player.reset()

		# ensure the player is in the center of the tile it is currently in
		self.player.adjust_position(player_tile.x + (player_tile.width - self.player.width) / 2,\
			player_tile.y + (player_tile.height - self.player.height) / 2)


class Tile(pygame.Rect):
	EMPTY_COLOUR = (255, 255, 255)
	OBSTACLE_COLOUR = (250, 100, 100)
	REWARD_COLOUR = (250, 250, 100)

	def __init__(self, x, y, size, board_x, board_y, tile_type):
		super().__init__(x, y, size, size)

		# tile variables
		self.board_x = board_x
		self.board_y = board_y
		self.change_type(tile_type)

	def change_type(self, tile_type):
		# change the tile type
		self.tile_type = tile_type

		# change the colour of the tile to the corresponding colour
		if self.tile_type == 'empty':
			self.colour = self.EMPTY_COLOUR
		elif self.tile_type == 'obstacle':
			self.colour = self.OBSTACLE_COLOUR
		elif self.tile_type == 'reward':
			self.colour = self.REWARD_COLOUR


class Player(pygame.Rect):
	NUM_MOVES = 4
	PLAYER_COLOUR = (0, 0, 0)
	DELTA_EPSILON = 0.0001

	def __init__(self, x, y, size, board_width, board_height):
		super().__init__(x, y, size, size)

		# player variables
		self.board_x = 0
		self.board_y = 0
		self.start_board_x = 0
		self.start_board_y = 0

		# board variables
		self.width_of_board = board_width
		self.height_of_board = board_height

		# q learning variables
		self.q_table = np.zeros((self.NUM_MOVES, board_height, board_width))
		self.action = None
		self.current_state = (self.board_x, self.board_y)
		self.previous_state = self.current_state
		self.epsilon = 1
		self.learning_rate = 1
		self.discount = 0.5

	def move(self, decrease_randomness):
		valid_move = False
		move = None
		state_moves = self.q_table[:, self.board_y, self.board_x]

		# save the current state (before moving)
		self.previous_state = self.current_state

		while not valid_move:
			# do a random action if a random number is less than the epsilon value, or all actions in this state are 0
			do_random = True if (random.random() < self.epsilon or all(move == 0 for move in state_moves)) else False

			if do_random:
				# pick a random action
				move = random.randint(0, self.NUM_MOVES)
			else:
				# do the action that has the highest number
				move = np.where(state_moves == np.max(state_moves))[0].tolist()
				if len(move) > 1:
					# more than one action with the highest number, pick one of those at random
					move = random.choice(move)
				else:
					# there is one clear action
					move = move[0]

			# check to see if this is a valid move
			valid_move = self.__do_move(move)

		# save the action that caused the moving
		self.action = move

		# save the current state (after moving)
		self.current_state = (self.board_x, self.board_y)

		# update epsilon if applicable
		if self.epsilon > 0 and decrease_randomness:
			self.epsilon -= self.DELTA_EPSILON

	def __do_move(self, move):
		if move == 0:
			# move up if possible
			if self.board_y - 1 < 0:
				# moving up is off the board
				return False
			else:
				# can move up
				self.board_y -= 1
				return True
		elif move == 1:
			# move down if possible
			if self.board_y + 1 > self.height_of_board - 1:
				# moving down is off the board
				return False
			else:
				# can move down
				self.board_y += 1
				return True
		elif move == 2:
			# move left if possible
			if self.board_x - 1 < 0:
				# moving left is off the board
				return False
			else:
				# can move left
				self.board_x -= 1
				return True
		elif move == 3:
			# move right if possible
			if self.board_x + 1 > self.width_of_board - 1:
				# moving right is off the board
				return False
			else:
				# can move right
				self.board_x += 1
				return True
		else:
			return False

	def update_table(self, reward):
		# q value of state before movement and the corresponding action taken
		current_q_value = self.q_table[self.action, self.previous_state[1], self.previous_state[0]]
		# array of possible actions for the state the player is currently in
		next_state_actions = self.q_table[:, self.current_state[1], self.current_state[0]]
		# update the q table according to https://en.wikipedia.org/wiki/Q-learning#Algorithm
		self.q_table[self.action, self.previous_state[1], self.previous_state[0]] = (1 - self.learning_rate) * current_q_value + self.learning_rate * (reward + self.discount * np.max(next_state_actions))

	def adjust_position(self, x, y):
		# set the player's position to the current arguments of the function
		self.x = x
		self.y = y

	def reset(self):
		# reset the player to the starting position
		self.board_x = self.start_board_x
		self.board_y = self.start_board_y
		self.action = None
		self.current_state = (self.board_x, self.board_y)
		self.previous_state = self.current_state










