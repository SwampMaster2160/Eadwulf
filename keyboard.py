from typing import Sequence

import pygame as pg


KEYCODES = [pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN, pg.K_RETURN, pg.K_ESCAPE]


class Keyboard:
	keys_pressed: Sequence[bool]
	keys_pressed_last_tick: Sequence[bool]
	keys_pressed_last_frame: Sequence[bool]
	keys_pressed_starting_now: dict
	new_text: str = ""

	def __init__(self):
		self.keys_pressed = pg.key.get_pressed()
		self.keys_pressed_last_tick = self.keys_pressed
		self.keys_pressed_last_frame = self.keys_pressed

	def get_ready_for_tick(self):
		self.keys_pressed = pg.key.get_pressed()
		self.keys_pressed_starting_now = {}
		for key in KEYCODES:
			self.keys_pressed_starting_now[key] = self.keys_pressed[key] and not self.keys_pressed_last_tick[key]
		self.keys_pressed_last_tick = self.keys_pressed

	def get_ready_for_frame(self):
		self.keys_pressed = pg.key.get_pressed()
		self.keys_pressed_starting_now = {}
		for key in KEYCODES:
			self.keys_pressed_starting_now[key] = self.keys_pressed[key] and not self.keys_pressed_last_frame[key]
		self.keys_pressed_last_frame = self.keys_pressed
