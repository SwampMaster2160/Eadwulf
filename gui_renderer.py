from enum import IntEnum
from typing import List, Optional

import pygame as pg
from pygame import Surface

from font_page import FontPage
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
	surfaces: List[Optional[Surface]]
	texture_dict: dict
	font_pages: List[FontPage]

	def __init__(self, texture_dict: dict, font_pages: List[FontPage]):
		self.texture_dict = texture_dict
		self.surfaces = [None] * 9
		self.font_pages = font_pages

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
				align = y * 3 + x
				if self.surfaces[align]:
					main_surface.blit(
						pg.transform.scale(
							self.surfaces[align],
							world_surface_on_screen_size
						), world_blit_offset)

	def init_surface(self, align: GUITextureAlign):
		if not self.surfaces[align]:
			self.surfaces[align] = Surface((256, 256), pg.SRCALPHA)

	def render_texture(self, texture, pos: PixelPos, align: GUITextureAlign):
		self.init_surface(align)
		self.surfaces[align].blit(self.texture_dict[texture], pos.to_tuple())

	def render_rect(self, color, pos: PixelPos, size: PixelPos, align: GUITextureAlign):
		self.init_surface(align)
		self.surfaces[align].fill(color, (pos.x, pos.y, size.x, size.y))

	def render_char(self, char: chr, pos: PixelPos, align: GUITextureAlign):
		char_id = ord(char)
		page = char_id // 256
		char_id_in_page = char_id % 256
		self.surfaces[align].blit(
			self.font_pages[page].texture, pos.to_tuple(), (char_id_in_page % 16 * 8, char_id_in_page // 16 * 16, 8, 16)
		)

	def render_string(self, string: str, centered: bool, pos: PixelPos, align: GUITextureAlign):
		width = 0
		for char in string:
			char_id = ord(char)
			page = char_id // 256
			char_id_in_page = char_id % 256
			width += self.font_pages[page].widths[char_id_in_page] + 1
		offset = 0
		if centered:
			offset = -(width - 1) // 2
		for char in string:
			char_id = ord(char)
			page = char_id // 256
			char_id_in_page = char_id % 256
			self.render_char(char, pos + PixelPos(offset, -8), align)
			offset += self.font_pages[page].widths[char_id_in_page] + 1
