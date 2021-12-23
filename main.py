import time

import pygame as pg

import render
import tick


def main():
	# Init window
	pg.init()
	windowed_size = (640, 480)
	screen = pg.display.set_mode(windowed_size, flags=pg.RESIZABLE, vsync=1)
	pg.display.set_caption("Eadwulf")
	fullscreen = 0
	
	# Init game vars
	last_time = time.time_ns()
	tick_time_carry = 0
	y = 0
	
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
							else:
								screen = pg.display.set_mode(windowed_size, pg.RESIZABLE, vsync=1)
		
		# Game ticks
		time_ns = time.time_ns()
		delta_time = time_ns - last_time + tick_time_carry
		last_time = time_ns
		for x in range(delta_time // 10000000):
			y = tick.tick(y)
		tick_time_carry = delta_time % 10000000
		
		# Render game
		render.render(screen, y)


if __name__ == "__main__":
	main()
