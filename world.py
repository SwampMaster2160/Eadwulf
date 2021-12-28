from chunk import Chunk
from keyboard import Keyboard
from player import Player
from tile_pos import TilePos
from tile_stack import TileStack
from world_renderer import WorldRenderer


class World:
	name: str = ""
	filepath: str = ""
	player: Player = Player()
	chunks: dict = {}

	def tick(self, keyboard: Keyboard):
		self.player.tick(keyboard, self)

	def render(self, world_renderer: WorldRenderer):
		for y in range(self.player.pos.y - 9, self.player.pos.y + 10):
			offset = -(world_renderer.world_surface_width_in_tiles // 2) + self.player.pos.x
			for x in range(offset, world_renderer.world_surface_width_in_tiles + offset):
				pos = TilePos(x, y)
				self[pos].render(world_renderer, pos)
		self.player.render(world_renderer)

	def __getitem__(self, item: TilePos) -> TileStack:
		chunk_pos = item.get_chunk_pos().get_tuple()
		if chunk_pos not in self.chunks:
			self.chunks[chunk_pos] = Chunk(item.get_chunk_pos())
			return self.chunks[chunk_pos][item.get_chunk_offset()]
		return self.chunks[chunk_pos][item.get_chunk_offset()]
