import pygame as pg


def render(screen, y: int):
	screen.fill((0, 0, 0))
	pg.draw.circle(screen, "red", (y, 100), 10)
	pg.display.flip()
