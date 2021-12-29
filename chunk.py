import threading
from typing import List, Optional

from chunk_pos import ChunkPos
from tile_pos import TilePos
from tile_stack import TileStack


class Chunk:
	tile_stacks: List[TileStack]

	def __init__(self, pos: ChunkPos):
		self.tile_stacks = [TileStack(TilePos(0, 0))] * 4096
		for y in range(pos.y * 64, pos.y * 64 + 64):
			for x in range(pos.x * 64, pos.x * 64 + 64):
				tile_pos = TilePos(x, y)
				self[tile_pos.get_chunk_offset()] = TileStack(tile_pos)

	def __getitem__(self, item: TilePos):
		return self.tile_stacks[item.y * 64 + item.x]

	def __setitem__(self, key: TilePos, value: TileStack):
		self.tile_stacks[key.y * 64 + key.x] = value


class ChunkGeneratorThread(threading.Thread):
	chunk: Optional[Chunk] = None
	pos: ChunkPos

	def __init__(self, pos: ChunkPos):
		super().__init__()
		self.pos = pos

	def run(self) -> None:
		self.chunk = Chunk(self.pos)
