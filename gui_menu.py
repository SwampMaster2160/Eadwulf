import copy
from typing import List, Tuple, Sequence

import pygame as pg

import gui_element
from game_state import GameState
from gui_element import GUIElement
from gui_renderer import GUIRenderer
from keyboard import Keyboard
from mouse_over_state import MouseOverState
from mouse_state import MouseState
from world import World


class GUIMenu:
	ELEMENTS: List[GUIElement] = []
	instance_elements: List[GUIElement]

	def __init__(self):
		self.instance_elements = copy.deepcopy(self.ELEMENTS)

	def esc_pressed(self):
		return None

	def tick(
			self, keyboard: Keyboard, mouse: MouseState, world: World
	) -> Tuple[GameState, any]:
		for element in self.instance_elements:
			element.tick(keyboard)
			is_mouse_over_return = element.is_mouse_over(mouse)
			mouse_over_state = MouseOverState.NOT_OVER
			if is_mouse_over_return:
				mouse_over_state = MouseOverState.HOVER_OVER
				if mouse.is_clicked:
					mouse_over_state = MouseOverState.CLICKING
				if mouse.is_clicked_starting_this_frame:
					click_return = element.click(world, self)
					if click_return is not None:
						return click_return
			if mouse.is_clicked_starting_this_frame and mouse_over_state == MouseOverState.NOT_OVER:
				element.click_off()
			element.hover_state = mouse_over_state

		if keyboard.keys_pressed_starting_now[pg.K_ESCAPE]:
			esc_pressed_return = self.esc_pressed()
			if esc_pressed_return is not None:
				return esc_pressed_return
		return GameState.IN_MENU, self

	def render(self, gui_renderer: GUIRenderer):
		for element in self.instance_elements:
			element.render(gui_renderer)


class PauseGUIMenu(GUIMenu):
	ELEMENTS = [
		gui_element.RectGUIElement(),
		gui_element.TextGUIElement("Game Paused"),
		gui_element.ResumeButton(auto_place_y=0),
		gui_element.ExitToMainMenuButton(auto_place_y=8),
		gui_element.ExitGameButton(auto_place_y=9)
	]

	def esc_pressed(self):
		return GameState.INGAME, self


class MainMenuGUIMenu(GUIMenu):
	ELEMENTS = [
		gui_element.RectGUIElement(),
		gui_element.TextGUIElement("Eadfulf"),
		gui_element.NewWorldButton(auto_place_y=0),
		gui_element.LoadWorldGUIButton(auto_place_y=1),
		gui_element.ExitGameButton(auto_place_y=9)
	]


class NewWorldGUIMenu(GUIMenu):
	ELEMENTS = [
		gui_element.RectGUIElement(),
		gui_element.TextEntryGUIElement("Name: ", auto_place_y=0),
		gui_element.TextGUIElement("Create New World?"),
		gui_element.NewWorldFinalizeButton(auto_place_y=8),
		gui_element.BackToMainMenuButton(auto_place_y=9)
	]
