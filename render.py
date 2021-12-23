import pygame as pg

from main import MainData


def render(main_data: MainData, screen, y: int):
	screen.fill((0, 0, 0))
	screen.blit(main_data.texture, (y, 100))
	screen.blit(main_data.texture2, (y * 2, y * 3))
	pg.display.flip()
