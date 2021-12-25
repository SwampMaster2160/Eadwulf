from enum import Enum, auto
from typing import Sequence, Tuple

import pygame as pg

import texture
from world_renderer import WorldRenderer


class PlayerState(Enum):
	IDLE = 0
	WALKING = auto()


class CardinalDirection(Enum):
	NORTH = auto()
	EAST = auto()
	SOUTH = auto()
	WEST = auto()


class Player:
	x: int = 0
	y: int = 0
	offset: int = 0
	player_state: PlayerState = PlayerState.IDLE
	facing: CardinalDirection = CardinalDirection.NORTH
	
	def tick(self, keys_pressed: Sequence[bool]):
		match self.player_state:
			case PlayerState.IDLE:
				is_w_pressed = keys_pressed[pg.K_w]
				is_a_pressed = keys_pressed[pg.K_a]
				is_s_pressed = keys_pressed[pg.K_s]
				is_d_pressed = keys_pressed[pg.K_d]
				if is_w_pressed or is_a_pressed or is_s_pressed or is_d_pressed:
					self.player_state = PlayerState.WALKING
					self.offset = 1
				if is_w_pressed:
					self.facing = CardinalDirection.NORTH
				elif is_a_pressed:
					self.facing = CardinalDirection.WEST
				elif is_s_pressed:
					self.facing = CardinalDirection.SOUTH
				elif is_d_pressed:
					self.facing = CardinalDirection.EAST
			case PlayerState.WALKING:
				self.offset += 1
				if self.offset > 15:
					self.player_state = PlayerState.IDLE
					self.offset = 0
					match self.facing:
						case CardinalDirection.NORTH:
							self.y -= 1
						case CardinalDirection.EAST:
							self.x += 1
						case CardinalDirection.SOUTH:
							self.y += 1
						case CardinalDirection.WEST:
							self.x -= 1
	
	def get_offset_x_and_y(self) -> Tuple[int, int]:
		x = 0
		y = 0
		match self.facing:
			case CardinalDirection.NORTH:
				y = -self.offset
			case CardinalDirection.EAST:
				x = self.offset
			case CardinalDirection.SOUTH:
				y = self.offset
			case CardinalDirection.WEST:
				x = -self.offset
		return x, y
	
	def render(self, world_renderer: WorldRenderer):
		player_texture = None
		match self.facing:
			case CardinalDirection.NORTH:
				player_texture = texture.PlayerNorth
			case CardinalDirection.EAST:
				player_texture = texture.PlayerEast
			case CardinalDirection.SOUTH:
				player_texture = texture.PlayerSouth
			case CardinalDirection.WEST:
				player_texture = texture.PlayerWest
		x_offset, y_offset = self.get_offset_x_and_y()
		world_renderer.render_texture(player_texture, (self.x * 16 + x_offset, self.y * 16 + y_offset))
