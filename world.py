import tile
from chunk import Chunk
from chunk_pos import ChunkPos
from player import Player
from tile_pos import TilePos
from tile_stack import TileStack
from world_renderer import WorldRenderer


class World:
	chunks: dict = {}

	def render(self, world_renderer: WorldRenderer, player: Player):
		for y in range(player.pos.y - 9, player.pos.y + 10):
			offset = -(world_renderer.world_surface_width_in_tiles // 2) + player.pos.x
			for x in range(offset, world_renderer.world_surface_width_in_tiles + offset):
				pos = TilePos(x, y)
				self[pos].render(world_renderer, pos)

	def __getitem__(self, item: TilePos) -> TileStack:
		chunk_pos = item.get_chunk_pos().get_tuple()
		if chunk_pos not in self.chunks:
			self.chunks[chunk_pos] = Chunk(item.get_chunk_pos())
			return self.chunks[chunk_pos][item.get_chunk_offset()]
		return self.chunks[chunk_pos][item.get_chunk_offset()]
