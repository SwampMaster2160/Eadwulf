import math

import pygame as pg
from pygame.surface import Surface

import texture
from common_data import CommonData
from player import CardinalDirection


def render(common_data: CommonData):
	# Calculate some pixel sizes and ratios
	window_aspect_ratio = common_data.window_size[0] / common_data.window_size[1]
	world_surface_width_in_tiles = math.ceil(window_aspect_ratio * 8) * 2 + 3
	
	# Create world drawing surface for drawing to
	world_surface = Surface((world_surface_width_in_tiles * 16, 304))
	world_surface.fill((0, 0, 0))
	
	# Draw
	for y in range(19):
		world_y = y - 9 + common_data.player.y
		for x in range(world_surface_width_in_tiles):
			world_x = x - (world_surface_width_in_tiles // 2) + common_data.player.x
			if world_x == 0 or world_y == 0:
				world_surface.blit(common_data.texture_dict[texture.Error], (x * 16, y * 16))
			else:
				world_surface.blit(common_data.texture_dict[texture.Grass], (x * 16, y * 16))
	common_data.player.render(common_data, world_surface, (
		(-(common_data.player.x - (world_surface_width_in_tiles // 2)) * 16),
		(-(common_data.player.y - 9) * 16)
	))
	
	# Calculate some scales and directions.
	tile_size = common_data.window_size[1] / 16
	pixel_size = common_data.window_size[1] / 256
	x_offset = 0
	y_offset = 0
	player_offset = common_data.player.offset
	match common_data.player.facing:
		case CardinalDirection.NORTH:
			y_offset = -player_offset
		case CardinalDirection.EAST:
			x_offset = player_offset
		case CardinalDirection.SOUTH:
			y_offset = player_offset
		case CardinalDirection.WEST:
			x_offset = -player_offset
	world_surface_on_screen_size = (world_surface_width_in_tiles * tile_size, 19 * tile_size)
	world_blit_offset = (
		-((world_surface_width_in_tiles * tile_size - common_data.window_size[0]) // 2) - (pixel_size * x_offset),
		-(tile_size * 1.5) - (pixel_size * y_offset)
	)
	# Blit world surface onto window surface
	common_data.screen.blit(pg.transform.scale(world_surface, world_surface_on_screen_size), world_blit_offset)
	pg.display.flip()
