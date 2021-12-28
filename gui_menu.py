import copy
from typing import List, Tuple, Sequence

import pygame as pg

import gui_element
from game_state import GameState
from gui_element import GUIElement
from gui_renderer import GUIRenderer, GUITextureAlign
from mouse_over_state import MouseOverState
from mouse_state import MouseState
from pixel_pos import PixelPos
from world import World


class GUIMenu:
	ELEMENTS: List[GUIElement] = []
	instance_elements: List[GUIElement]

	def __init__(self):
		self.instance_elements = copy.deepcopy(self.ELEMENTS)

	def esc_pressed(self):
		return None

	def tick(self, keys_pressed: Sequence[bool], keys_pressed_this_frame: dict, mouse: MouseState, world: World) -> Tuple[GameState, any]:
		for element in self.instance_elements:
			is_mouse_over_return = element.is_mouse_over(mouse)
			mouse_over_state = MouseOverState.NOT_OVER
			if is_mouse_over_return:
				mouse_over_state = MouseOverState.HOVER_OVER
				if mouse.is_clicked:
					mouse_over_state = MouseOverState.CLICKING
				if mouse.is_clicked_starting_this_frame:
					click_return = element.click(world)
					if click_return is not None:
						return click_return
			element.hover_state = mouse_over_state

		if keys_pressed_this_frame[pg.K_ESCAPE]:
			esc_pressed_return = self.esc_pressed()
			if esc_pressed_return is not None:
				return esc_pressed_return
		return GameState.IN_MENU, self

	def render(self, gui_renderer: GUIRenderer):
		for element in self.instance_elements:
			element.render(gui_renderer)


class PauseGUIMenu(GUIMenu):
	ELEMENTS = [
		gui_element.RectGUIElement(PixelPos(0, 0), PixelPos(100, 100), (127, 127, 127), GUITextureAlign.CENTRE_CENTRE),
		gui_element.ButtonGUIElement(PixelPos(150, 20), PixelPos(100, 100), GUITextureAlign.CENTRE_CENTRE)
	]

	def esc_pressed(self):
		return GameState.INGAME, self
