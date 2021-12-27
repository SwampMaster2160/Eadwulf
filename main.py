import os
import time

import pygame as pg

from gui_renderer import GUIRenderer
from player import Player
from texture import Texture
from world import World
from world_renderer import WorldRenderer


KEYCODES = [pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN, pg.K_RETURN]


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
	keys_pressed_last_tick = pg.key.get_pressed()
	
	player = Player()
	world = World()
	
	# Load all textures
	main_dir = os.path.split(os.path.abspath(__file__))[0]
	texture_dict = {}
	for texture_class in Texture.__subclasses__():
		texture_dict[texture_class] = pg.image.load(
			os.path.join(main_dir, "res", "texture", texture_class.FILENAME + ".png"))
	
	# Main game loop
	running = 1
	while running:
		# Poll window events
		for event in pg.event.get():
			match event.type:
				case pg.QUIT:
					running = 0
				case pg.KEYUP:
					match event.key:
						case pg.K_F11:
							fullscreen = not fullscreen
							if fullscreen:
								windowed_size = pg.display.get_window_size()
								main_surface = pg.display.set_mode(flags=pg.FULLSCREEN, vsync=1)
							else:
								main_surface = pg.display.set_mode(windowed_size, pg.RESIZABLE, vsync=1)
		
		# Game ticks
		time_ns = time.time_ns()
		delta_time = time_ns - last_time + tick_time_carry
		last_time = time_ns
		for x in range(delta_time // 10000000):
			keys_pressed = pg.key.get_pressed()
			keys_pressed_this_tick = {}
			for key in KEYCODES:
				keys_pressed_this_tick[key] = keys_pressed[key] and not keys_pressed_last_tick[key]

			player.tick(keys_pressed, keys_pressed_this_tick, world)

			keys_pressed_last_tick = keys_pressed
		tick_time_carry = delta_time % 10000000
		
		# Render game
		world_renderer = WorldRenderer(main_surface, texture_dict, player)
		gui_renderer = GUIRenderer(texture_dict)
		
		world.render(world_renderer, player)
		player.render(world_renderer)
		player.render_gui(gui_renderer)
		
		world_renderer.blit_onto_main_surface(main_surface, player)
		gui_renderer.blit_onto_main_surface(main_surface)
		pg.display.flip()


if __name__ == "__main__":
	main()
