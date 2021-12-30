from typing import List, Optional

import texture
import tile
from tile import Tile
from tile_pos import TilePos
from world_renderer import WorldRenderer


class TileStack:
	tiles: List[Tile] = []

	def __init__(self, pos: Optional[TilePos]):
		if pos is None:
			self.tiles = []
			return
		ground_height = pos.perlin(420420, 1, 5, 0)
		sand_type_map = pos.perlin(420420, 4, 6, 4)
		if ground_height < 18:
			if sand_type_map < 24:
				self.tiles = [tile.SandTile()]
			elif sand_type_map < 32:
				self.tiles = [tile.BlackSandTile()]
			else:
				self.tiles = [tile.GravelTile()]
		elif ground_height > 22:
			self.tiles = [tile.GrassTile(), tile.TreeTile()]
		else:
			self.tiles = [tile.GrassTile()]
			foliage_map = pos.random(420420, 7)
			if foliage_map > 0.95:
				self.tiles.append(tile.TreeTile())
			elif foliage_map > 0.85:
				self.tiles.append(tile.FlowersTile())
		if ground_height < 16:
			self.tiles.append(tile.WaterTile())

	def render(self, world_renderer: WorldRenderer, pos: TilePos):
		for x, chunk_tile in enumerate(self.tiles):
			chunk_tile.render(world_renderer, pos, self, x)
		if not self.tiles:
			world_renderer.render_texture(texture.PitBottomTexture, pos.get_pixel_pos())

	def can_walk(self, player):
		if not self.tiles:
			return 1
		return self.tiles[-1].can_walk(player)
