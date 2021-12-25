import math

import pygame as pg
from pygame.surface import Surface

from pixel_pos import PixelPos


class WorldRenderer:
	surface: Surface
	texture_dict: dict
	world_origin: PixelPos
	world_surface_width_in_tiles: int
	
	def __init__(self, main_surface: Surface, texture_dict: dict, player):
		window_size = main_surface.get_size()
		self.texture_dict = texture_dict
		self.world_surface_width_in_tiles = math.ceil(window_size[0] / window_size[1] * 8) * 2 + 3
		self.surface = Surface((self.world_surface_width_in_tiles * 16, 304))
		self.world_origin = PixelPos(
			(-(player.pos.x - (self.world_surface_width_in_tiles // 2)) * 16),
			(-(player.pos.y - 9) * 16)
		)
		
	def blit_onto_main_surface(self, main_surface: Surface, player):
		window_size = main_surface.get_size()
		tile_size = window_size[1] / 16
		pixel_size = window_size[1] / 256
		offset = player.get_offset_x_and_y()
		world_surface_on_screen_size = (self.world_surface_width_in_tiles * tile_size, 19 * tile_size)
		world_blit_offset = (
			-((self.world_surface_width_in_tiles * tile_size - window_size[0]) // 2) - (
						pixel_size * offset.x),
			-(tile_size * 1.5) - (pixel_size * offset.y)
		)
		main_surface.blit(pg.transform.scale(self.surface, world_surface_on_screen_size), world_blit_offset)
	
	def render_texture(self, texture, pos: PixelPos):
		self.surface.blit(self.texture_dict[texture], (self.world_origin + pos).to_tuple())
