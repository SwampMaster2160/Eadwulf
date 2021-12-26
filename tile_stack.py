from typing import List

from tile import Tile
from tile_pos import TilePos
from world_renderer import WorldRenderer


class TileStack:
	tiles: List[Tile] = []

	def __init__(self, tiles: List[Tile]):
		self.tiles = tiles

	def render(self, world_renderer: WorldRenderer, pos: TilePos):
		for tile in self.tiles:
			tile.render(world_renderer, pos)
