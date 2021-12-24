from enum import Enum, auto

from pygame.surface import Surface

import texture
from common_data import CommonData


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
	
	def render(self, common_data: CommonData, surface: Surface,  world_origin_on_world_surface: tuple):
		world_origin_on_world_surface_x = world_origin_on_world_surface[0]
		world_origin_on_world_surface_y = world_origin_on_world_surface[1]
		x_offset = 0
		y_offset = 0
		player_texture = None
		match self.facing:
			case CardinalDirection.NORTH:
				y_offset = -self.offset
				player_texture = common_data.texture_dict[texture.PlayerNorth]
			case CardinalDirection.EAST:
				x_offset = self.offset
				player_texture = common_data.texture_dict[texture.PlayerEast]
			case CardinalDirection.SOUTH:
				y_offset = self.offset
				player_texture = common_data.texture_dict[texture.PlayerSouth]
			case CardinalDirection.WEST:
				x_offset = -self.offset
				player_texture = common_data.texture_dict[texture.PlayerWest]
		surface.blit(player_texture, (
			world_origin_on_world_surface_x + 16 * self.x + x_offset,
			world_origin_on_world_surface_y + 16 * self.y + y_offset
		))
