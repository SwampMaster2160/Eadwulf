import math
import os

import pygame as pg
from pygame.surface import Surface

import texture
from common_data import CommonData


def render(common_data: CommonData):
	# Calculate some pixel sizes and ratios
	window_aspect_ratio = common_data.window_size[0] / common_data.window_size[1]
	world_surface_width_in_tiles = math.ceil(window_aspect_ratio * 8) * 2 + 3
	
	# Create world drawing surface for drawing to
	world_surface = Surface((world_surface_width_in_tiles * 16, 304))
	world_surface.fill((0, 0, 0))
	
	# Draw
	for y in range(19):
		world_y = y - 9
		for x in range(world_surface_width_in_tiles):
			world_x = x - (world_surface_width_in_tiles // 2)
			if world_x == 0 or world_y == 0:
				world_surface.blit(common_data.texture_dict[texture.Error], (x * 16, y * 16))
			else:
				world_surface.blit(common_data.texture_dict[texture.Grass], (x * 16, y * 16))
	
	# Scale the world surface and blit it onto the screen surface
	tile_size = common_data.window_size[1] / 16
	pixel_size = common_data.window_size[1] / 256
	world_surface_on_screen_size = (world_surface_width_in_tiles * tile_size, 19 * tile_size)
	world_blit_offset = (-((world_surface_width_in_tiles * tile_size - common_data.window_size[0]) // 2), -(tile_size * 1.5))
	common_data.screen.blit(pg.transform.scale(world_surface, world_surface_on_screen_size), world_blit_offset)
	pg.display.flip()
