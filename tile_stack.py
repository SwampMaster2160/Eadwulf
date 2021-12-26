import random
from typing import List

import tile
from tile import Tile
from tile_pos import TilePos
from world_renderer import WorldRenderer


class TileStack:
	tiles: List[Tile] = []

	def __init__(self, pos: TilePos):
		if pos.x == 0 or pos.y == 0 or random.randint(0, 1):
			self.tiles = [tile.WaterTile()]
		else:
			self.tiles = [tile.GrassTile()]
			if random.randint(0, 1):
				self.tiles.append(tile.TreeTile())

	def render(self, world_renderer: WorldRenderer, pos: TilePos):
		for tile in self.tiles:
			tile.render(world_renderer, pos)
