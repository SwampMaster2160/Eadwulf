import itertools
import os
import time

import pygame as pg
from pygame.event import Event

import gui_menu
from font_page import FontPage
from game_state import GameState
from gui_renderer import GUIRenderer
from keyboard import Keyboard
from mouse import Mouse
from simple_thread import SimpleThread
from texture import Texture
from world import World
from world_renderer import WorldRenderer


def main():
	# Init window
	pg.init()
	main_surface = pg.display.set_mode(flags=pg.FULLSCREEN, vsync=1)
	windowed_size = (640, 480)
	pg.display.set_caption("Eadwulf")
	fullscreen = 1
	
	# Init game vars
	last_time = time.time_ns()
	tick_time_carry = 0
	keyboard = Keyboard()
	mouse = Mouse()

	world = World()
	game_state = GameState.IN_MENU
	current_gui_menu = gui_menu.MainMenuGUIMenu(world)
	
	# Load all textures
	main_dir = os.path.split(os.path.abspath(__file__))[0]
	texture_dict = {}
	for texture_class in Texture.__subclasses__():
		texture_dict[texture_class] = pg.image.load(
			os.path.join(main_dir, "res", "texture", texture_class.FILENAME + ".png"))

	font_pages = []
	for x in itertools.count():
		try:
			font_pages.append(FontPage(x))
		except FileNotFoundError:
			break
	
	# Main game loop
	running = 1
	while running:
		keyboard.new_text = ""
		# Poll window events
		for event in pg.event.get():
			match event.type:
				case pg.QUIT:
					if world.do_save_world:
						world.save()
					world.do_save_world = 0
					running = 0
				case pg.KEYDOWN:
					keyboard.new_text += event.unicode
				case pg.KEYUP:
					match event.key:
						case pg.K_F11:
							fullscreen = not fullscreen
							if fullscreen:
								windowed_size = pg.display.get_window_size()
								main_surface = pg.display.set_mode(flags=pg.FULLSCREEN, vsync=1)
							else:
								main_surface = pg.display.set_mode(windowed_size, pg.RESIZABLE, vsync=1)
				case pg.MOUSEMOTION:
					mouse.pos = event.pos
				case pg.MOUSEBUTTONUP:
					if event.button == pg.BUTTON_LEFT:
						mouse.is_clicked_starting_this_frame = 1
						mouse.is_clicked = 0
				case pg.MOUSEBUTTONDOWN:
					if event.button == pg.BUTTON_LEFT:
						mouse.is_clicked = 1

		# Game ticks
		time_ns = time.time_ns()
		delta_time = time_ns - last_time + tick_time_carry
		last_time = time_ns
		for x in range(delta_time // 10000000):
			keyboard.get_ready_for_tick()
			if game_state == GameState.INGAME:
				world.tick(keyboard)
		tick_time_carry = delta_time % 10000000

		# Each frame (Not rendering)
		gui_renderer = GUIRenderer(texture_dict, font_pages)
		mouse.calculate_surface_poses(main_surface.get_size(), gui_renderer)
		keyboard.get_ready_for_frame()

		if keyboard.keys_pressed_starting_now[pg.K_ESCAPE] and game_state == GameState.INGAME:
			game_state = GameState.IN_MENU
			current_gui_menu = gui_menu.PauseGUIMenu(world)
		elif game_state == GameState.IN_MENU:
			game_state, current_gui_menu = current_gui_menu.tick(keyboard, mouse, world)
		
		# Render game
		world_renderer = WorldRenderer(main_surface, texture_dict, world.player)

		world_render_thread = SimpleThread(World.render, (world, world_renderer))
		world_render_thread.start()

		match game_state:
			case GameState.INGAME:
				world.player.render_gui(gui_renderer)
			case GameState.IN_MENU:
				current_gui_menu.render(gui_renderer)

		world_render_thread.join()

		world_renderer.blit_onto_main_surface(main_surface, world.player)
		gui_renderer.blit_onto_main_surface(main_surface)
		pg.display.flip()

		# End
		mouse.is_clicked_starting_this_frame = 0

		if game_state == GameState.EXITING:
			pg.event.post(Event(pg.QUIT))


if __name__ == "__main__":
	main()
