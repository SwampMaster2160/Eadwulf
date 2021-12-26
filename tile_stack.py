from typing import List

import tile
from tile import Tile
from tile_pos import TilePos
from world_renderer import WorldRenderer


class TileStack:
	tiles: List[Tile] = []

	def __init__(self, pos: TilePos):
		if pos.x == 0 or pos.y == 0:
			self.tiles = [tile.Tile()]
		else:
			self.tiles = [tile.GrassTile()]

	def render(self, world_renderer: WorldRenderer, pos: TilePos):
		for tile in self.tiles:
			tile.render(world_renderer, pos)
