import random
from typing import List

import tile
from tile import Tile
from tile_pos import TilePos
from world_renderer import WorldRenderer


class TileStack:
	tiles: List[Tile] = []

	def __init__(self, pos: TilePos):
		if pos.perlin(42042034, 1, 5) < 16:
			self.tiles = [tile.WaterTile()]
		else:
			self.tiles = [tile.GrassTile()]
			if pos.random(42042034, 5) > 0.95:
				self.tiles.append(tile.TreeTile())

	def render(self, world_renderer: WorldRenderer, pos: TilePos):
		for chunk_tile in self.tiles:
			chunk_tile.render(world_renderer, pos)
