from enum import IntEnum
from typing import List

import pygame as pg
from pygame import Surface

from pixel_pos import PixelPos


class GUITextureAlign(IntEnum):
	TOP_LEFT = 0
	TOP_CENTRE = 1
	TOP_RIGHT = 2
	CENTRE_LEFT = 3
	CENTRE_CENTRE = 4
	CENTRE_RIGHT = 5
	BOTTOM_LEFT = 6
	BOTTOM_CENTRE = 7
	BOTTOM_RIGHT = 8


class GUIRenderer:
	surfaces: List[Surface]
	texture_dict: dict

	def __init__(self, texture_dict: dict):
		self.texture_dict = texture_dict
		self.surfaces = [Surface((256, 256), pg.SRCALPHA) for x in range(9)]

	def blit_onto_main_surface(self, main_surface: Surface):
		window_size = main_surface.get_size()
		pixel_size = window_size[1] // 256
		world_surface_on_screen_size = (256 * pixel_size, 256 * pixel_size)
		for y in range(3):
			y_offset = 0
			match y:
				case 1:
					y_offset = window_size[1] // 2 - pixel_size * 128
				case 2:
					y_offset = window_size[1] - pixel_size * 256
			for x in range(3):
				x_offset = 0
				match x:
					case 1:
						x_offset = window_size[0] // 2 - pixel_size * 128
					case 2:
						x_offset = window_size[0] - pixel_size * 256
				world_blit_offset = (x_offset, y_offset)
				main_surface.blit(
					pg.transform.scale(
						self.surfaces[y * 3 + x],
						world_surface_on_screen_size
					), world_blit_offset)

	def render_texture(self, texture, pos: PixelPos, align: GUITextureAlign):
		self.surfaces[align].blit(self.texture_dict[texture], pos.to_tuple())

	def render_rect(self, color, pos: PixelPos, size: PixelPos, align: GUITextureAlign):
		self.surfaces[align].fill(color, (pos.x, pos.y, size.x, size.y))
