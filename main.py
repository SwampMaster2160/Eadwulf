import os
import time

import pygame as pg

import render
import tick
from common_data import CommonData
from player import Player
from texture import Texture


def main():
	common_data = CommonData()
	
	# Init window
	pg.init()
	common_data.screen = pg.display.set_mode((640, 480), flags=pg.RESIZABLE, vsync=1)
	windowed_size = pg.display.get_window_size()
	common_data.window_size = windowed_size
	pg.display.set_caption("Eadwulf")
	fullscreen = 0
	common_data.player = Player()
	
	# Init game vars
	last_time = time.time_ns()
	tick_time_carry = 0
	y = 0
	
	main_dir = os.path.split(os.path.abspath(__file__))[0]
	for texture in Texture.__subclasses__():
		common_data.texture_dict[texture] = pg.image.load(os.path.join(main_dir, "res", "texture", texture.FILENAME + ".png"))
	
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
								common_data.screen = pg.display.set_mode(flags=pg.FULLSCREEN, vsync=1)
								common_data.window_size = pg.display.get_window_size()
							else:
								common_data.screen = pg.display.set_mode(windowed_size, pg.RESIZABLE, vsync=1)
								common_data.window_size = pg.display.get_window_size()
				case pg.VIDEORESIZE:
					common_data.window_size = pg.display.get_window_size()
		
		# Game ticks
		time_ns = time.time_ns()
		delta_time = time_ns - last_time + tick_time_carry
		last_time = time_ns
		for x in range(delta_time // 10000000):
			tick.tick(common_data)
		tick_time_carry = delta_time % 10000000
		
		# Render game
		render.render(common_data)


if __name__ == "__main__":
	main()
