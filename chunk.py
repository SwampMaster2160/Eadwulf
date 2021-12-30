import os
import pathlib
import pickle
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


class ChunkGetterThread(threading.Thread):
	chunk: Optional[Chunk] = None
	pos: ChunkPos
	world_filename: str

	def __init__(self, pos: ChunkPos, world_filename: str):
		super().__init__()
		self.pos = pos
		self.world_filename = world_filename

	def run(self) -> None:
		try:
			world_path = os.path.join(pathlib.Path.home(), "eadwulf", "world", self.world_filename, "chunks")
			filename = f"{self.pos.get_tuple()[0]}_{self.pos.get_tuple()[1]}.ech"
			file = open(os.path.join(world_path, filename), "rb")
			self.chunk = pickle.load(file)
			file.close()
		except FileNotFoundError:
			self.chunk = Chunk(self.pos)
