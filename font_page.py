import os
from typing import List

import pygame as pg
from pygame.surface import Surface


class FontPage:
	texture: Surface
	widths: List[int]

	def __init__(self, page: int):
		main_dir = os.path.split(os.path.abspath(__file__))[0]
		self.texture = pg.image.load(
			os.path.join(main_dir, "res", "texture", "font", str(page) + ".png"))
		widths_file = open(os.path.join(main_dir, "res", "texture", "font", str(page) + ".cwt"), "rb")
		self.widths = [byte for byte in widths_file.read()]
		widths_file.close()
