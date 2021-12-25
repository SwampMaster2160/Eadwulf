import math
import os
import time

import pygame as pg
from pygame.surface import Surface

from player import Player, CardinalDirection
from texture import Texture
from world import World
from world_renderer import WorldRenderer


def main():
	# Init window
	pg.init()
	screen = pg.display.set_mode((640, 480), flags=pg.RESIZABLE, vsync=1)
	windowed_size = pg.display.get_window_size()
	window_size = windowed_size
	pg.display.set_caption("Eadwulf")
	fullscreen = 0
	
	# Init game vars
	last_time = time.time_ns()
	tick_time_carry = 0
	
	player = Player()
	world = World()
	world_renderer = WorldRenderer()
	
	main_dir = os.path.split(os.path.abspath(__file__))[0]
	world_renderer.texture_dict = {}
	for texture_class in Texture.__subclasses__():
		world_renderer.texture_dict[texture_class] = pg.image.load(
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
								screen = pg.display.set_mode(flags=pg.FULLSCREEN, vsync=1)
								window_size = pg.display.get_window_size()
							else:
								screen = pg.display.set_mode(windowed_size, pg.RESIZABLE, vsync=1)
								window_size = pg.display.get_window_size()
				case pg.VIDEORESIZE:
					window_size = pg.display.get_window_size()
		
		# Game ticks
		time_ns = time.time_ns()
		delta_time = time_ns - last_time + tick_time_carry
		last_time = time_ns
		for x in range(delta_time // 10000000):
			player.tick(pg.key.get_pressed())
		tick_time_carry = delta_time % 10000000
		
		# Render game
		
		# Calculate some pixel sizes and ratios and create world renderer surface.
		world_renderer.world_surface_width_in_tiles = math.ceil(window_size[0] / window_size[1] * 8) * 2 + 3
		world_renderer.surface = Surface((world_renderer.world_surface_width_in_tiles * 16, 304))
		world_renderer.world_origin = (
			(-(player.x - (world_renderer.world_surface_width_in_tiles // 2)) * 16),
			(-(player.y - 9) * 16)
		)
		
		# Draw
		world.render(world_renderer, player)
		player.render(world_renderer)
		
		# Blit the world renderer onto the screen.
		tile_size = window_size[1] / 16
		pixel_size = window_size[1] / 256
		x_offset, y_offset = player.get_offset_x_and_y()
		world_surface_on_screen_size = (world_renderer.world_surface_width_in_tiles * tile_size, 19 * tile_size)
		world_blit_offset = (
			-((world_renderer.world_surface_width_in_tiles * tile_size - window_size[0]) // 2) - (pixel_size * x_offset),
			-(tile_size * 1.5) - (pixel_size * y_offset)
		)
		screen.blit(pg.transform.scale(world_renderer.surface, world_surface_on_screen_size), world_blit_offset)
		pg.display.flip()


if __name__ == "__main__":
	main()
