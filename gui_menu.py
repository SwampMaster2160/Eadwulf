import copy
from typing import List, Tuple, Sequence

import pygame as pg

import gui_element
from game_state import GameState
from gui_element import GUIElement
from gui_renderer import GUIRenderer, GUITextureAlign
from pixel_pos import PixelPos


class GUIMenu:
	ELEMENTS: List[GUIElement] = []
	instance_elements: List[GUIElement]

	def __init__(self):
		self.instance_elements = copy.deepcopy(self.ELEMENTS)

	def tick(self, keys_pressed: Sequence[bool], keys_pressed_this_frame: dict) -> Tuple[GameState, any]:
		return GameState.IN_MENU, self

	def render(self, gui_renderer: GUIRenderer):
		for element in self.instance_elements:
			element.render(gui_renderer)


class PauseGUIMenu(GUIMenu):
	ELEMENTS = [gui_element.RectGUIElement(PixelPos(0, 0), PixelPos(100, 100), (127, 127, 127), GUITextureAlign.CENTRE_CENTRE)]

	def tick(self, keys_pressed: Sequence[bool], keys_pressed_this_frame: dict) -> Tuple[GameState, any]:
		new_game_state = GameState.IN_MENU
		if keys_pressed_this_frame[pg.K_ESCAPE]:
			new_game_state = GameState.INGAME
		return new_game_state, self
