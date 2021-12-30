import os
import pathlib
import pickle

from chunk import ChunkGetterThread, Chunk
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
	do_save_world: bool = 0
	ticks_since_last_save: int = 0

	def start_using_generated_chunks(self):
		for pos, generating_chunk in self.chunks.items():
			if isinstance(generating_chunk, ChunkGetterThread) and not generating_chunk.is_alive():
				self.chunks[pos] = generating_chunk.chunk

	def tick(self, keyboard: Keyboard):
		self.start_using_generated_chunks()
		self.player.tick(keyboard, self)
		self.ticks_since_last_save += 1
		if self.ticks_since_last_save > 1000:
			self.save()
			self.ticks_since_last_save = 0

	def render(self, world_renderer: WorldRenderer):
		self.start_using_generated_chunks()
		for y in range(self.player.pos.y - 9, self.player.pos.y + 10):
			offset = -(world_renderer.world_surface_width_in_tiles // 2) + self.player.pos.x
			for x in range(offset, world_renderer.world_surface_width_in_tiles + offset):
				pos = TilePos(x, y)
				self[pos].render(world_renderer, pos)
		self.player.render(world_renderer)

	def __getitem__(self, item: TilePos) -> TileStack:
		chunk_pos = item.get_chunk_pos().get_tuple()
		if chunk_pos not in self.chunks:
			self.chunks[chunk_pos] = ChunkGetterThread(item.get_chunk_pos(), self.filepath)
			self.chunks[chunk_pos].start()
			return TileStack(None)
		elif isinstance(self.chunks[chunk_pos], ChunkGetterThread):
			return TileStack(None)
		return self.chunks[chunk_pos][item.get_chunk_offset()]

	def new(self, filename: str):
		if len(filename) < 1:
			return 0
		if "/" in filename or "\\" in filename:
			return 0
		try:
			world_path = os.path.join(pathlib.Path.home(), "eadwulf", "world", filename, "chunks")
			os.makedirs(world_path)
		except OSError:
			return 0
		self.name = filename
		self.filepath = filename
		self.chunks = {}
		self.do_save_world = 1
		self.player = Player()
		return 1

	def load(self, path: str):
		self.filepath = path
		self.chunks = {}
		self.player = Player()
		self.do_save_world = 1

	def save(self):
		save_delete_pos = self.player.pos.get_chunk_pos()
		print("Save")
		world_path = os.path.join(pathlib.Path.home(), "eadwulf", "world", self.filepath, "chunks")
		os.makedirs(world_path, exist_ok=1)
		to_del = []
		for pos, chunk in self.chunks.items():
			if isinstance(chunk, Chunk):
				filename = f"{pos[0]}_{pos[1]}.ech"
				file = open(os.path.join(world_path, filename), "wb")
				pickle.dump(chunk, file)
				file.close()
				if pos[1] < save_delete_pos.y - 1 or save_delete_pos.y + 1 < pos[1]:
					to_del.append(pos)
		for pos in to_del:
			del self.chunks[pos]
