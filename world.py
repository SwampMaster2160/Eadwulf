import texture
import tile
from player import Player
from tile_pos import TilePos
from tile_stack import TileStack
from world_renderer import WorldRenderer


class World:
	def render(self, world_renderer: WorldRenderer, player: Player):
		for y in range(player.pos.y - 9, player.pos.y + 10):
			offset = -(world_renderer.world_surface_width_in_tiles // 2) + player.pos.x
			for x in range(offset, world_renderer.world_surface_width_in_tiles + offset):
				pos = TilePos(x, y)
				self[pos].render(world_renderer, pos)

	def __getitem__(self, item: TilePos) -> TileStack:
		if item.x == 0 or item.y == 0:
			return TileStack([tile.Tile()])
		return TileStack([tile.GrassTile()])
